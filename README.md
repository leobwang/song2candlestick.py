# 🎼📈 Song2Candlestick

A unique music visualization tool that transforms MIDI piano performances into dynamic candlestick charts, creating a mesmerizing fusion of musical and financial data visualization.

## ✨ Features

- **🎵 Real-time Audio Playback**: Synchronized audio playback using pygame backend
- **📊 Individual Note Candlesticks**: Each piano note becomes a unique candlestick with randomized OHLC values
- **🎨 Dynamic Color Coding**: 
  - 🟢 **Green** when open > close
  - 🔴 **Red** when open < close  
  - ⚪ **Light Gray** when open = close
- **🖤 Sleek Dark Theme**: Professional black background with white text and grid
- **📱 Sliding Window Display**: Shows the most recent 32 candlesticks for optimal viewing
- **🎹 MIDI Support**: Works with any MIDI file containing piano tracks

## 🎯 How It Works

The system takes each individual note from the first instrument (typically piano) in a MIDI file and generates candlestick data:

- **High** = `note_pitch + uniform(0, 3)`
- **Low** = `note_pitch + uniform(-3, 0)`
- **Open** = `uniform(low, high)`
- **Close** = `uniform(low, high)`

Each candlestick appears in perfect synchronization with the music playback, creating a unique trading-chart-style visualization of the musical performance.

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Conda (recommended for environment management)

### Setup

1. **Clone or download the project**:
   ```bash
   cd your-projects-directory
   # Copy song2candlestick.py to your desired location
   ```

2. **Create conda environment and install Python dependencies**:
   ```bash
   conda create -y python=3.12 --name music0
   conda activate music0
   pip install -r requirements.txt
   ```

3. **Install system dependencies**:
   ```bash
   # macOS (using Homebrew)
   brew install fluid-synth
   
   # Ubuntu/Debian
   sudo apt-get install fluidsynth
   
   # Windows
   # Download FluidSynth from https://www.fluidsynth.org/
   ```

4. **Install audio synthesis dependencies**:
   ```bash
   conda install -c conda-forge pyfluidsynth fluidsynth
   ```

## 🚀 Usage

1. **Prepare your MIDI file**:
   - Place your MIDI file in an accessible location
   - Update the file path in `song2candlestick.py`:
   ```python
   song = pretty_midi.PrettyMIDI("path/to/your/midi/file.mid")
   ```

2. **Run the visualization**:
   ```bash
   conda activate music0
   python song2candlestick.py
   ```

3. **Enjoy the show**! 🎭
   - Audio will start playing automatically
   - Candlesticks will appear synchronized with the music
   - The display window shows 32 candlesticks at a time in a sliding window

## 📁 Project Structure

```
song2candlestick/
├── song2candlestick.py    # Main visualization script
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── filepath.txt           # Optional file path storage
```

## 🎼 Example Output

The system processes each note from the piano track and creates a unique candlestick visualization:

- **3,648 individual notes** (example from Hungarian Rhapsody No. 2)
- **533+ seconds** of synchronized audio and visual content
- **Professional trading-chart aesthetics** with musical data
- **Smooth real-time animation** at 50ms intervals

## 🎛️ Customization

### Change MIDI File
```python
# Edit this line in song2candlestick.py
song = pretty_midi.PrettyMIDI("your/path/to/file.mid")
```

### Adjust Display Window Size
```python
# In _update_plot method, change MAX_DISPLAY value
MAX_DISPLAY = 32  # Show 32 candlesticks (default)
```

### Modify Color Scheme
```python
# In _draw_candlestick method
if open_val > close:
    color = '#00AA00'  # Green - customize this
elif open_val < close:
    color = '#FF3333'  # Red - customize this
else:
    color = '#CCCCCC'  # Gray - customize this
```

### Adjust OHLC Randomization
```python
# In _calculate_candlestick_data method
high = pitch + np.random.uniform(0, 3)    # Customize range
low = pitch + np.random.uniform(-3, 0)    # Customize range
```

## 🐛 Troubleshooting

### Audio Issues
- **PortAudio errors**: The system automatically falls back to pygame audio
- **No sound**: Check your system audio settings and ensure pygame is installed
- **SDL warnings**: These are harmless compatibility messages and can be ignored

### Performance Issues
- **Slow rendering**: Reduce the number of candlesticks displayed by changing `MAX_DISPLAY`
- **Memory usage**: Large MIDI files with many notes will use more memory

### MIDI File Issues
- **Instrument not found**: Ensure your MIDI file has at least one instrument
- **No notes**: Check that `instruments[0]` contains note data

## 🎵 Tested With

- **Hungarian Rhapsody No. 2** by Franz Liszt (3,648 notes, 533 seconds)
- Various classical piano pieces
- Multi-instrument MIDI files (uses first instrument only)

## 🤝 Contributing

Feel free to fork, modify, and enhance this unique music visualization tool! Some ideas for improvements:

- Support for multiple instruments simultaneously
- Different chart types (line charts, bar charts, etc.)
- Interactive controls for playback speed
- Export capabilities for animations
- Different randomization algorithms for OHLC data

## 📄 License

This project is open source. Use and modify as needed for your creative projects!

## 🙏 Acknowledgments

- **pretty_midi**: For excellent MIDI file processing
- **matplotlib**: For powerful plotting capabilities  
- **pygame**: For reliable audio playback
- **numpy**: For efficient numerical operations

---

**Enjoy turning your favorite piano pieces into mesmerizing candlestick visualizations!** 🎹📊✨
