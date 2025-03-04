import streamlit as st
from streamlit.components.v1 import html
# Conversion factors dictionary (moved to global scope)
CONVERSION_FACTORS = {
    'length': {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'millimeters': 0.001,
        'miles': 1609.34,
        'yards': 0.9144,
        'feet': 0.3048,
        'inches': 0.0254
    },
    'weight': {
        'kilograms': 1,
        'grams': 0.001,
        'milligrams': 1e-6,
        'metric tons': 1000,
        'pounds': 0.453592,
        'ounces': 0.0283495
    },
    'temperature': {
        'celsius': lambda c: c,
        'fahrenheit': lambda f: (f - 32) * 5/9,
        'kelvin': lambda k: k - 273.15
    },
    'volume': {
        'liters': 1,
        'milliliters': 0.001,
        'cubic meters': 1000,
        'cubic centimeters': 0.001,
        'cubic feet': 28.3168,
        'gallons (US)': 3.78541,
        'gallons (UK)': 4.54609
    },
    'area': {
        'square meters': 1,
        'square kilometers': 1e6,
        'square miles': 2.58999e6,
        'square yards': 0.836127,
        'square feet': 0.092903,
        'square inches': 0.00064516,
        'hectares': 10000,
        'acres': 4046.86
    }
}

# Conversion functions
def convert(value, from_unit, to_unit, category):
    if category == 'temperature':
        # Convert to Celsius first
        celsius = CONVERSION_FACTORS[category][from_unit](value)
        # Convert to target unit
        if to_unit == 'celsius':
            return celsius
        elif to_unit == 'fahrenheit':
            return (celsius * 9/5) + 32
        elif to_unit == 'kelvin':
            return celsius + 273.15
    else:
        factor = CONVERSION_FACTORS[category][from_unit]
        value_in_base = value * factor
        return value_in_base / CONVERSION_FACTORS[category][to_unit]

# Streamlit UI
st.set_page_config(page_title="Unit Converter For GIAIC", page_icon="📐", layout="centered")

# Custom CSS
st.header  ("  UNIT CONVERTER WITH FORMULA ")
st.markdown("""
<style>
    .h1 {UNIT CONVERTER WITH FORMULAS}
    .main { background-color: GRAY }
    .stTextInput input { font-size: 18px !important; }
    .unit-section { 
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .header { color: #5f6368; font-size: 14px; font-weight: 500; }
   
    .conversion-item { 
        padding: 10px 0;
        border-bottom: 1px solid #e0e0e0;
        font-size: 14px;
    }
    .category-btn {
        padding: 16px 16px;
        margin: 0 5px;
        border-radius: 20px;
        border: 1px solid #dadce0;
        background: white;
        color: #5f6368;
        cursor: pointer;
    }
    .category-btn.active {
        background: #f1f3f4;
        border-color: #f1f3f4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'category' not in st.session_state:
    st.session_state.category = 'length'
if 'from_unit' not in st.session_state:
    st.session_state.from_unit = 'meters'
if 'to_unit' not in st.session_state:
    st.session_state.to_unit = 'kilometers'
if 'input_value' not in st.session_state:
    st.session_state.input_value = 1.0

# Category selection
categories = {
    'Length': 'length',
    'Weight': 'weight',
    'Temperature': 'temperature',
    'Volume': 'volume',
    'Area': 'area'
}

cols = st.columns(len(categories))
for idx, (name, cat) in enumerate(categories.items()):
    with cols[idx]:
        if st.button(name, key=f"cat_{cat}", 
                     help=f"Convert {name.lower()} units",
                     use_container_width=True):
            st.session_state.category = cat

# Conversion section
with st.container():
    st.markdown('<div class="unit-section">', unsafe_allow_html=True)
    
    # From/To units
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="header">FROM</div>', unsafe_allow_html=True)
        from_unit = st.selectbox(
            label="From unit",
            options=list(CONVERSION_FACTORS[st.session_state.category].keys()),
            label_visibility="collapsed",
            key="from_unit_selectbox"
        )
        
    with col2:
        st.markdown('<div class="header">TO</div>', unsafe_allow_html=True)
        to_unit = st.selectbox(
            label="To unit",
            options=list(CONVERSION_FACTORS[st.session_state.category].keys()),
            label_visibility="collapsed",
            key="to_unit_selectbox"
        )
    
    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        input_value = st.number_input(
            label="Input value",
            value=st.session_state.input_value,
            key="input_value",
            label_visibility="collapsed"
        )
    
    with col2:
        try:
            result = convert(input_value, from_unit, to_unit, st.session_state.category)
            st.text_input(
                label="Result",
                value=f"{result:.6f}".rstrip('0').rstrip('.') if isinstance(result, float) else result,
                disabled=True,
                key="result"
            )
        except:
            st.error("Invalid conversion")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Common conversions section
st.markdown('<div class="unit-section">', unsafe_allow_html=True)
st.markdown('<div class="header">COMMON CONVERSIONS</div>', unsafe_allow_html=True)

# Get 5 common units (excluding selected ones)
common_units = [u for u in CONVERSION_FACTORS[st.session_state.category].keys() 
                if u not in [from_unit, to_unit]][:5]

for unit in common_units:
    try:
        converted = convert(input_value, from_unit, unit, st.session_state.category)
        col1, col2 = st.columns([3,7])
        with col1:
            st.markdown(f"**{input_value} {from_unit}**")
        with col2:
            st.markdown(f"= {converted:.6f}".rstrip('0').rstrip('.') + f" {unit}")
        st.markdown('<div class="conversion-item"></div>', unsafe_allow_html=True)
    except:
        pass

# Conversion factors dictionary (moved to global scope)
CONVERSION_FACTORS = {
    'length': {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'millimeters': 0.001,
        'miles': 1609.34,
        'yards': 0.9144,
        'feet': 0.3048,
        'inches': 0.0254
    },
    'weight': {
        'kilograms': 1,
        'grams': 0.001,
        'milligrams': 1e-6,
        'metric tons': 1000,
        'pounds': 0.453592,
        'ounces': 0.0283495
    },
    'temperature': {
        'celsius': lambda c: c,
        'fahrenheit': lambda f: (f - 32) * 5/9,
        'kelvin': lambda k: k - 273.15
    },
    'volume': {
        'liters': 1,
        'milliliters': 0.001,
        'cubic meters': 1000,
        'cubic centimeters': 0.001,
        'cubic feet': 28.3168,
        'gallons (US)': 3.78541,
        'gallons (UK)': 4.54609
    },
    'area': {
        'square meters': 1,
        'square kilometers': 1e6,
        'square miles': 2.58999e6,
        'square yards': 0.836127,
        'square feet': 0.092903,
        'square inches': 0.00064516,
        'hectares': 10000,
        'acres': 4046.86
    }
}

# Conversion function (modified to use global CONVERSION_FACTORS)
def convert(value, from_unit, to_unit, category):
    if category == 'temperature':
        # Convert to Celsius first
        celsius = CONVERSION_FACTORS[category][from_unit](value)
        # Convert to target unit
        if to_unit == 'celsius':
            return celsius
        elif to_unit == 'fahrenheit':
            return (celsius * 9/5) + 32
        elif to_unit == 'kelvin':
            return celsius + 273.15
    else:
        factor = CONVERSION_FACTORS[category][from_unit]
        value_in_base = value * factor
        return value_in_base / CONVERSION_FACTORS[category][to_unit]

# Common conversions section (modified)
common_units = [u for u in CONVERSION_FACTORS[st.session_state.category].keys() 
               if u not in [from_unit, to_unit]][:5]

# Footer
st.markdown("""
<div style="text-align: center; color: #5f6368; font-size: 12px; margin-top: 20px;">
    Unit Converter - from MUHAMMAD RAFAY SHAHZAD
</div>
""", unsafe_allow_html=True)