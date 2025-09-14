import pretty_midi
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import threading
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load MIDI file
song = pretty_midi.PrettyMIDI(open("filepath.txt").read())

class MusicCandlestickPlotter:
    def __init__(self, midi_file):
        self.midi_file = midi_file
        self.instrument = midi_file.instruments[0]  # Use instrument[0] as specified
        self.candlestick_data = self._calculate_candlestick_data()
        
        # Playback variables
        self.audio_data = None
        self.sample_rate = 44100
        self.start_time = None
        self.current_candlestick_index = 0
        self.playback_speed = 1.0  # Speed multiplier for visualization
        
        # Plot setup with black background
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        
        # Set black background
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        
        # Set text colors to white for visibility
        self.ax.set_title('Music Candlestick Chart - One Candlestick Per Note\n(Green: open>close, Red: open<close, Light Gray: open=close)', 
                         fontsize=12, color='white')
        self.ax.set_xlabel('Notes (Chronological Order)', fontsize=12, color='white')
        self.ax.set_ylabel('Pitch (MIDI Note Number)', fontsize=12, color='white')
        
        # White grid on black background
        self.ax.grid(True, alpha=0.3, color='white')
        
        # Set tick colors to white
        self.ax.tick_params(colors='white')
        
        # Set spine colors to white
        for spine in self.ax.spines.values():
            spine.set_color('white')
        
        # Store candlestick patches for animation
        self.candlestick_patches = []
        
    def _calculate_candlestick_data(self):
        """Calculate candlestick data for each individual note with randomized OHLC values"""
        candlestick_data = []
        
        # Sort notes by start time
        sorted_notes = sorted(self.instrument.notes, key=lambda n: n.start)
        
        for i, note in enumerate(sorted_notes):
            pitch = note.pitch
            
            # Calculate OHLC values as specified:
            # high = pitch + uniform(0, 3)
            # low = pitch + uniform(-3, 0)
            # open = uniform(low, high)
            # close = uniform(low, high)
            
            high = pitch + np.random.uniform(0, 3)
            low = pitch + np.random.uniform(-3, 0)
            
            # Open and close are random values between low and high
            open_val = np.random.uniform(low, high)
            close_val = np.random.uniform(low, high)
            
            candlestick_data.append({
                'time': note.start,
                'index': i,
                'open': open_val,
                'high': high,
                'low': low,
                'close': close_val,
                'pitch': pitch,
                'duration': note.end - note.start
            })
        
        return candlestick_data
    
    def _synthesize_audio(self):
        """Synthesize audio from MIDI for playback"""
        print("Synthesizing audio...")
        self.audio_data = self.midi_file.fluidsynth(fs=self.sample_rate)
        print(f"Audio synthesized: {len(self.audio_data)/self.sample_rate:.2f} seconds")
    
    def _draw_candlestick(self, data, alpha=1.0):
        """Draw a single candlestick with unified colors"""
        x = data['display_index']  # Use display_index for positioning
        open_val, high, low, close = data['open'], data['high'], data['low'], data['close']
        
        # Determine color based on corrected logic - same color for all components:
        # green if open > close, red if open < close, light gray if open = close
        if open_val > close:
            color = '#00AA00'  # Bright green
        elif open_val < close:
            color = '#FF3333'  # Bright red
        else:
            color = '#CCCCCC'  # Light gray (visible on black background)
        
        # Use the same color for line, fill, and edge
        line_color = color
        fill_color = color
        edge_color = color
        
        # Draw the high-low line (wick)
        line = self.ax.plot([x, x], [low, high], color=line_color, linewidth=1.5, alpha=alpha)[0]
        
        # Draw the open-close rectangle (body)
        body_height = abs(close - open_val) if open_val != close else 0.3  # minimum height for visibility
        body_bottom = min(open_val, close) if open_val != close else close - 0.15
        
        rect = Rectangle((x - 0.35, body_bottom), 0.7, body_height, 
                        facecolor=fill_color, edgecolor=edge_color, linewidth=1, alpha=alpha)
        self.ax.add_patch(rect)
        
        return line, rect
    
    def _update_plot(self, frame):
        """Animation update function with sliding window of max 32 candlesticks"""
        if self.start_time is None:
            return
        
        # Calculate elapsed time since start
        elapsed_time = time.time() - self.start_time
        
        # Find current position in the song (accounting for playback speed)
        current_song_time = elapsed_time * self.playback_speed
        
        # Find how many candlesticks should be visible
        new_index = 0
        for i, data in enumerate(self.candlestick_data):
            if data['time'] <= current_song_time:
                new_index = i + 1
            else:
                break
        
        # Implement sliding window: show max 32 candlesticks
        MAX_DISPLAY = 32
        
        # Calculate which candlesticks should be visible
        if new_index <= MAX_DISPLAY:
            # Show from beginning
            start_index = 0
            end_index = new_index
        else:
            # Sliding window: show the most recent 32
            start_index = new_index - MAX_DISPLAY
            end_index = new_index
        
        # Clear the plot if we need to slide the window
        if hasattr(self, 'last_start_index') and start_index != self.last_start_index:
            self.ax.clear()
            
            # Restore black background and white text after clearing
            self.ax.set_facecolor('black')
            self.ax.set_title('Music Candlestick Chart - One Candlestick Per Note\n(Green: open>close, Red: open<close, Light Gray: open=close)', 
                             fontsize=12, color='white')
            self.ax.set_xlabel('Notes (Chronological Order)', fontsize=12, color='white')
            self.ax.set_ylabel('Pitch (MIDI Note Number)', fontsize=12, color='white')
            self.ax.grid(True, alpha=0.3, color='white')
            
            # Set tick and spine colors to white
            self.ax.tick_params(colors='white')
            for spine in self.ax.spines.values():
                spine.set_color('white')
                
            self.candlestick_patches = []
            self.current_candlestick_index = start_index
        
        self.last_start_index = start_index
        
        # Draw new candlesticks
        while self.current_candlestick_index < end_index and self.current_candlestick_index < len(self.candlestick_data):
            data = self.candlestick_data[self.current_candlestick_index].copy()
            # Set display index relative to window start
            data['display_index'] = self.current_candlestick_index - start_index
            line, rect = self._draw_candlestick(data)
            self.candlestick_patches.append((line, rect))
            self.current_candlestick_index += 1
        
        # Update plot limits for sliding window
        if end_index > start_index:
            self.ax.set_xlim(-1, MAX_DISPLAY)
            
            # Get y-limits from currently visible data
            visible_data = self.candlestick_data[start_index:end_index]
            if visible_data:
                all_highs = [d['high'] for d in visible_data]
                all_lows = [d['low'] for d in visible_data]
                y_margin = 2
                self.ax.set_ylim(min(all_lows) - y_margin, max(all_highs) + y_margin)
        
        return []
    
    def play_with_visualization(self, enable_audio=True):
        """Start audio playback and visualization simultaneously"""
        audio_working = False
        
        if enable_audio:
            try:
                if self.audio_data is None:
                    self._synthesize_audio()
                
                # Try different audio backends
                print("Testing audio backends...")
                import sounddevice as sd_test
                
                # Try to list available devices
                devices = sd_test.query_devices()
                print(f"Available audio devices: {len(devices)}")
                
                # Try to find a working output device
                default_device = sd_test.default.device[1]  # output device
                print(f"Using audio device: {default_device}")
                
                # Test audio output with simpler approach
                test_audio = np.sin(2 * np.pi * 440 * np.linspace(0, 0.1, int(0.1 * self.sample_rate)))
                sd_test.play(test_audio, self.sample_rate, device=default_device)
                sd_test.wait()
                audio_working = True
                print("Audio system working!")
                
            except Exception as e:
                print(f"Audio playback failed: {e}")
                print("Trying alternative audio method...")
                
                try:
                    # Alternative: use pygame for audio if available
                    import pygame
                    pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=4096)
                    
                    # Convert audio to pygame format
                    audio_int16 = (self.audio_data * 32767).astype(np.int16)
                    sound = pygame.sndarray.make_sound(audio_int16)
                    
                    def play_pygame_audio():
                        self.start_time = time.time()
                        sound.play()
                        # Wait for sound to finish
                        while pygame.mixer.get_busy():
                            time.sleep(0.1)
                    
                    audio_thread = threading.Thread(target=play_pygame_audio)
                    audio_thread.daemon = True
                    audio_thread.start()
                    audio_working = True
                    print("Using pygame audio backend!")
                    
                except ImportError:
                    print("pygame not available")
                    audio_working = False
                except Exception as e2:
                    print(f"pygame audio also failed: {e2}")
                    audio_working = False
        
        print("Starting visualization...")
        
        if audio_working and 'sd_test' in locals():
            # Start audio playback in a separate thread
            def play_audio():
                try:
                    self.start_time = time.time()
                    sd_test.play(self.audio_data, self.sample_rate, device=default_device)
                    sd_test.wait()  # Wait until audio finishes
                except Exception as e:
                    print(f"Audio playback error: {e}")
            
            if 'pygame' not in locals():  # Only start thread if not using pygame
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.daemon = True
                audio_thread.start()
        elif not audio_working:
            # Start timer for visualization without audio (speed up 4x)
            self.playback_speed = 4.0
            self.start_time = time.time()
            print(f"Running visualization at {self.playback_speed}x speed (no audio)")
        
        # Start animation
        ani = animation.FuncAnimation(self.fig, self._update_plot, interval=50, blit=False)
        
        plt.tight_layout()
        plt.show()
        
        return ani

# Create and run the candlestick plotter
print("Initializing Music Candlestick Plotter...")
plotter = MusicCandlestickPlotter(song)

print(f"Found {len(plotter.candlestick_data)} individual notes")
print(f"Using instrument: {plotter.instrument.name}")
print("Each candlestick represents one note with randomized OHLC variations")

# Start the visualization
ani = plotter.play_with_visualization()
