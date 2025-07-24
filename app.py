import streamlit as st
from PIL import Image, ImageColor
import io
import numpy as np

# Basic Pantone-to-HEX dictionary (expand as needed)
pantone_to_hex = {
    "Pantone Green Olive": "#708238",
    "Pantone Moroccan Blue": "#0f4c81",
    "Pantone White": "#ffffff",
    "Pantone Black": "#000000"
}

st.title("Fabric Pattern Visualizer")

# Upload the base pattern image
pattern_file = st.file_uploader("Upload a pattern file", type=["png", "jpg", "jpeg"])

# Input Pantone fabric and print colors
fabric_pantone = st.text_input("Fabric Color (Pantone name)", "Pantone Moroccan Blue")
print_pantone = st.text_input("Print Color (Pantone name)", "Pantone Green Olive")

# Check if colors exist
fabric_hex = pantone_to_hex.get(fabric_pantone, None)
print_hex = pantone_to_hex.get(print_pantone, None)

# Show color swatches
if fabric_hex:
    st.markdown(f"<div style='width:100px;height:30px;background-color:{fabric_hex};border:1px solid #000;padding:5px;text-align:center;'>Fabric</div>", unsafe_allow_html=True)
if print_hex:
    st.markdown(f"<div style='width:100px;height:30px;background-color:{print_hex};border:1px solid #000;padding:5px;text-align:center;'>Print</div>", unsafe_allow_html=True)

if pattern_file and fabric_hex and print_hex:
    # Load and convert pattern to grayscale
    pattern = Image.open(pattern_file).convert("L")
    pattern = pattern.point(lambda x: 255 if x < 128 else 0, '1')  # Binarize

    # Convert to numpy array for pixel manipulation
    arr = np.array(pattern)

    # Create RGB image
    rgb_image = np.zeros((arr.shape[0], arr.shape[1], 3), dtype=np.uint8)

    fabric_rgb = ImageColor.getrgb(fabric_hex)
    print_rgb = ImageColor.getrgb(print_hex)

    rgb_image[arr == 255] = fabric_rgb    # background (white areas)
    rgb_image[arr == 0] = print_rgb       # pattern (black areas)

    final_image = Image.fromarray(rgb_image)

    st.image(final_image, caption="Preview: Fabric + Print Colors", use_column_width=True)

    # Allow download
    output = io.BytesIO()
    final_image.save(output, format="PNG")
    st.download_button(
        label="Download Mockup",
        data=output.getvalue(),
        file_name="pattern_mockup.png",
        mime="image/png"
    )

elif pattern_file and (not fabric_hex or not print_hex):
    st.error("One or both Pantone color names are not recognized. Please use a supported name.")

st.markdown("""
Supported Pantone names:
- Pantone Green Olive
- Pantone Moroccan Blue
- Pantone White
- Pantone Black

(You can expand this list with more Pantone colors later.)
""")
