import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io

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

if pattern_file and fabric_hex and print_hex:
    pattern = Image.open(pattern_file).convert("RGBA")

    # Create a background layer for the fabric color
    bg = Image.new("RGBA", pattern.size, fabric_hex)

    # Tint the pattern using the print color (multiplying over background)
    overlay = Image.new("RGBA", pattern.size, print_hex + "AA")  # semi-transparent overlay
    combined = Image.alpha_composite(bg, overlay)
    final_image = Image.alpha_composite(combined, pattern)

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