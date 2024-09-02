import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

def lookup_standard_sack_size(chemical_name):
    """Lookup the standard sack size for a given chemical."""
    return standard_sack_sizes.get(chemical_name, "Unknown")

# Decision Tree Functions
def stoppit_decision_tree(loss_rate, diamond_seal_available=None):
    if loss_rate < 25:
        return [
            {"Chemical": "STOPPIT", "Concentration (ppb)": int(50)},
        ], []
    elif 25 <= loss_rate < 50:
        return [
            {"Chemical": "STOPPIT", "Concentration (ppb)": int(80)},
        ], []
    elif 50 <= loss_rate < 100:
        if diamond_seal_available is None:
            return "Checking DIAMOND SEAL availability..."
        elif diamond_seal_available:
            return [
                {"Chemical": "STOPPIT", "Concentration (ppb)": int(120)},
                {"Chemical": "DIAMOND SEAL", "Concentration (ppb)": int(10)},
                {"Chemical": "NaCl", "Concentration (ppb)": int(1)}
            ], []
        else:
            return [
                {"Chemical": "STOPPIT", "Concentration (ppb)": int(120)},
                {"Chemical": "HYDRO-PLUG", "Concentration (ppb)": int(40)},
                {"Chemical": "Note", "Concentration": "", "Notes": "Pill Volume: 300-ft open hole minimum, pump this pill as water base and through a Treating Sub/Open ended."}
            ], []
    elif 100 <= loss_rate < 150:
        if diamond_seal_available is None:
            return "Checking DIAMOND SEAL availability..."
        elif diamond_seal_available:
            return [
                {"Chemical": "STOPPIT", "Concentration (ppb)": int(120)},
                {"Chemical": "DIAMOND SEAL", "Concentration (ppb)": int(10)},
                {"Chemical": "NaCl", "Concentration (ppb)": int(1)},
                {"Chemical": "BAROLIFT", "Concentration (ppb)": int(1)}
            ], []
        else:
            return [
                {"Chemical": "STOPPIT", "Concentration (ppb)": int(120)},
                {"Chemical": "BaraLock-666.M", "Concentration (ppb)": int(0.25)},
                {"Chemical": "BaraLock-666.C", "Concentration (ppb)": int(0.2)},
                {"Chemical": "Note", "Concentration": "", "Notes": "Pill Volume: 300-ft open hole minimum, pump this pill as water base and through a Treating Sub/Open ended."}
            ], []
    elif loss_rate >= 150:
        return [
            {"Chemical": "BaraBlend-665", "Concentration (ppb)": int(100)},
            {"Chemical": "BaraLock-666.M", "Concentration (ppb)": int(0.25)},
            {"Chemical": "BaraLock-666.C", "Concentration (ppb)": int(0.2)},
            {"Chemical": "Note", "Concentration": "", "Notes": "Pump this pill as water base and through a Treating Sub/Open ended."}
        ], []
    else:
        return "Invalid loss rate"

def barablend_657_decision_tree(loss_rate):
    if loss_rate < 25:
        return [
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(50)},
            {"Chemical": "Note", "Concentration": "", "Notes": "Pill Volume: 200-ft open hole"}
        ], []
    elif 25 <= loss_rate < 50:
        return [
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(80)},
            {"Chemical": "Note", "Concentration": "", "Notes": "Have the 80 ppb pill ready and pump it at the first occurrence of losses"}
        ], []
    elif 50 <= loss_rate < 100:
        return [
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(100)},
            {"Chemical": "BARAFLAKE C", "Concentration (ppb)": int(20)},
            {"Chemical": "Note", "Concentration": "", "Notes": "Pill Volume: 300-ft open hole minimum, pump this pill as water base and through a Treating Sub/Open ended."}
        ], []
    elif 100 <= loss_rate < 150:
        return [
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(120)},
            {"Chemical": "BARAFLAKE C", "Concentration (ppb)": int(40)},
            {"Chemical": "Note", "Concentration": "", "Notes": "Pill Volume: 300-ft open hole minimum, pump this pill as water base and through a Treating Sub/Open ended."}
        ], []
    elif loss_rate >= 150:
        return [
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(120)},
            {"Chemical": "BaraLock-666.M", "Concentration (ppb)": int(0.25)},
            {"Chemical": "BaraLock-666.C", "Concentration (ppb)": int(0.25)},
            {"Chemical": "Note", "Concentration": "", "Notes": "Pump this pill as water base and through a Treating Sub/Open ended."}
        ], []
    else:
        return "Invalid loss rate"

def non_reservoir_decision_tree(loss_rate):
    secondary_table = []
    if loss_rate < 15:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(40)},
            {"Chemical": "CaCO3 Flake F", "Concentration (ppb)": int(10)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(10)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(10)}
        ]
    elif 15 <= loss_rate < 50:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(80)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 F", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(10)},
            {"Chemical": "Quickseal F", "Concentration (ppb)":int(10)},
            {"Chemical": "Mica M", "Concentration (ppb)": int(10)},
            {"Chemical": "Mica C", "Concentration (ppb)": int(20)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(80)},
            {"Chemical": "STOPPIT", "Concentration (ppb)": int(70)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(10)}
        ]
    elif 50 <= loss_rate < 100:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration": "100 ppb", "Notes": ""},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(20)},
            {"Chemical": "Mica M", "Concentration (ppb)": int(20)},
            {"Chemical": "Mica F", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 F", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 M", "Concentration": "20 ppb", "Notes": ""},
            {"Chemical": "Quickseal F", "Concentration (ppb)":int(10)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(100)},
            {"Chemical": "STOPPIT", "Concentration (ppb)": int(80)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(10)}
        ]
    elif 100 <= loss_rate < 200:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(120)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(20)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(10)},
            {"Chemical": "Nutplug F", "Concentration (ppb)": int(20)},
            {"Chemical": "Quickseal M", "Concentration (ppb)":int(20)},
            {"Chemical": "Mica C", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 C", "Concentration (ppb)": int(10)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(120)},
            {"Chemical": "STOPPIT", "Concentration (ppb)": int(100)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(10)}
        ]
    elif loss_rate >= 200:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(160)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(20)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(20)},
            {"Chemical": "Nutplug F", "Concentration (ppb)": int(10)},
            {"Chemical": "Quickseal F", "Concentration (ppb)":int(20)},
            {"Chemical": "Quickseal C", "Concentration (ppb)":int(15)},
            {"Chemical": "Mica M", "Concentration (ppb)": int(20)},
            {"Chemical": "Mica C", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(25)},
            {"Chemical": "CaCO3 C", "Concentration (ppb)": int(15)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(160)},
            {"Chemical": "STOPPIT", "Concentration (ppb)": int(120)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(20)}
        ]
    else:
        primary_table = "Invalid loss rate"
    
    return primary_table, secondary_table

def reservoir_decision_tree(loss_rate):
    secondary_table = []
    if loss_rate < 15:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(40)},
            {"Chemical": "CaCO3 Flake F", "Concentration (ppb)": int(10)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(10)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(10)}
        ]
    elif 15 <= loss_rate < 50:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(80)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 F", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(15)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 Flake C", "Concentration (ppb)": int(20)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(80)},
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(50)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(15)}
        ]
    elif 50 <= loss_rate < 100:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(100)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(25)},
            {"Chemical": "BAROFIBRE M", "Concentration (ppb)": int(25)},
            {"Chemical": "CaCO3 M", "Concentration (ppb)": int(25)},
            {"Chemical": "CaCO3 C", "Concentration (ppb)": int(10)},
            {"Chemical": "CaCO3 Flake C", "Concentration (ppb)": int(10)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(100)},
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(80)},
            {"Chemical": "BAROFIBRE M", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 Flake F", "Concentration (ppb)": int(25)}
        ]
    elif 100 <= loss_rate < 200:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(120)},
            {"Chemical": "BARAFIBRE SF", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(30)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(30)},
            {"Chemical": "CaCO3 Flake C", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 Flake F", "Concentration (ppb)": int(20)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(120)},
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(80)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(20)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(20)}
        ]
    elif loss_rate >= 200:
        primary_table = [
            {"Chemical": "LCM Pill", "Concentration (ppb)": int(160)},
            {"Chemical": "CaCO3 F", "Concentration (ppb)": int(15)},
            {"Chemical": "CaCO3 Flake F", "Concentration (ppb)": int(25)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(25)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(25)},
            {"Chemical": "CaCO3 C", "Concentration (ppb)": int(25)},
            {"Chemical": "CaCO3 Flake C", "Concentration (ppb)": int(25)}
        ]
        secondary_table = [
            {"Chemical": "Speciality LCM Pill", "Concentration (ppb)": int(160)},
            {"Chemical": "BaraBlend-657", "Concentration (ppb)": int(10)},
            {"Chemical": "BAROFIBRE O", "Concentration (ppb)": int(30)},
            {"Chemical": "CaCO3 Flake M", "Concentration (ppb)": int(30)}
        ]
    else:
        primary_table = "Invalid loss rate"
    
    return primary_table, secondary_table


# Define the standard sack sizes
standard_sack_sizes = {
    "BaraBlend-657": 22.6796,
    "BaraBlend-665": 25.0,
    "BaraLock-666.C": 25.0,
    "BaraLock-666.M": 25.0,
    "BARACARB 5": 25.0,
    "BARACARB 25": 25.0,
    "BARACOR 100": 55.0,
    "BARADEFOAM W-300": [5.0, 55.0],
    "BAROFIBRE M": 11.3398,
    "BARAFIBRE SF": 11.3398,
    "BAROFIBRE O": 11.3398,
    "BARAFLAKE C": 22.6796,
    "BARAFLAKE M": 22.6796,
    "BARANEX": 22.6796,
    "BARASHILD 982": 22.6796,
    "BARITE 4.1": 1000.0,
    "BARITE": 1500.0,
    "BAROID RIG WASH": 55.0,
    "BENTONITE": 1000.0,
    "Biocide": 5.0,
    "CaCO3 C": 25.0,
    "CaCO3 F": 25.0,
    "CaCO3 Flake C": 22.6796,
    "CaCO3 Flake F": 22.6796,
    "CaCO3 Flake M": 22.6796,
    "CaCO3 M": 25.0,
    "CAUSTIC SODA": 25.0,
    "CITRIC ACID": 25.0,
    "DIAMOND SEAL": 25.0,
    "DRILLING DETERGENT": 55.0,
    "DRILTREAT": 55.0,
    "EP LUBE": 55.0,
    "EZ MUD": 5.0,
    "EZ MUL NT": 55.0,
    "GELTONE II": 22.6796,
    "HYDRO-PLUG": 25.0,
    "INVERMUL-NT": 55.0,
    "LIME": 25.0,
    "Mica C": 25.0,
    "Mica F": 25.0,
    "Mica M": 25.0,
    "MUSOL Solvent": 55.0,
    "Nutplug C": 25.0,
    "Nutplug F": 25.0,
    "Nutplug M": 25.0,
    "PAC L": 25.0,
    "POTASSIUM CARBONATE": 1000000.0,
    "POTASSIUM HYDROXIDE": 25.0,
    "POTASSIUM SULFATE": 1000.0,
    "Quickseal C": 25.0,
    "Quickseal F": 25.0,
    "Quickseal M": 25.0,
    "SODA ASH": 25.0,
    "SODIUM BICARBONATE": 25.0,
    "SODIUM FORMATE": 1000000.0,
    "STEELSEAL 50": 22.6796,
    "STEELSEAL 100": 22.6796,
    "STOPPIT": 25.0,
    "SUSPENSION PACKAGE II": 22.6796,
    "ZINC CARBONATE": 25.0,
    "NaCl": 25.0,
    "BAROLIFT": 25.0
}

# Function to show recommendation table
def show_recommendation():
    if 'recommendation_list' in st.session_state:
        recommendations = st.session_state['recommendation_list']
        if isinstance(recommendations, str):
            st.write(recommendations)
        else:
            recommendation_df = pd.DataFrame(recommendations)
            st.write("### Treatment Recommendations:")
            st.dataframe(recommendation_df.style.highlight_max(axis=0))
            st.markdown("---")
            
            # Bar chart for concentrations
            recommendation_df['Concentration'] = recommendation_df['Concentration'].apply(lambda x: float(x.split()[0]) if x else 0)
            fig = px.bar(recommendation_df, x='Chemical', y='Concentration', title='Treatment Concentrations', labels={'Concentration': 'Concentration (ppb)'})
            st.px_chart(fig)
            
            # Save recommendations to CSV
            csv = recommendation_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Recommendations as CSV",
                data=csv,
                file_name='recommendations.csv',
                mime='text/csv',
            )

# Streamlit app layout
def main():
    st.set_page_config(page_title="Lost Circulation Treatment Decision Tree", layout="wide")

    st.markdown("""
        <style>
            .main {
                background-color: #1e1e1e;
                color: #f0f0f5;
                padding: 20px;
            }
            .sidebar .sidebar-content {
                background-color: #1e1e1e;
                color: #f0f0f5;
                padding: 20px;
            }
            .stButton>button {
                color: #1e1e1e;
                background-color: #ff4b4b;
                border-radius: 10px;
            }
            .stRadio>label {
                font-size: 16px;
                color: #f0f0f5;
            }
            .stNumberInput>label {
                font-size: 16px;
                color: #f0f0f5;
            }
            .stSelectbox>label {
                font-size: 16px;
                color: #f0f0f5;
            }
            .stMarkdown {
                color: #f0f0f5;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Welcome to Lost Circulation Treatment Program")
    st.write("Developer: Amaresh Mishra")

    st.sidebar.header("Input Parameters")
    formation_type = st.sidebar.selectbox("Select Formation Type:", [
        "Permeable Sandstone type of formations",
        "Reservoir Zone",
        "Non-Reservoir Zone",
        "Formations requiring Acid solubility",
    ])

    st.sidebar.subheader("Steps:")
    st.sidebar.markdown("1. **Reduce ROP and Monitor Loss rate**")
    st.sidebar.markdown("2. **Reduce circulation rate/Stop circulation - monitor for dynamic vs. static losses**")

    st.sidebar.markdown("### Notes")
    notes = st.sidebar.text_area("Please provide any notes or report issues:")
    if st.sidebar.button("Submit Notes"):
        st.sidebar.write("Thank you for your notes!")

    st.header("Treatment Inputs")

    if formation_type == "Permeable Sandstone type of formations":
     is_well_flowing = st.radio("Is the well flowing?", ["Yes", "No"])
     if is_well_flowing == "Yes":
        st.write("Refer to Well Control Procedures.")
     else:
        diamond_seal_available = st.radio("Is DIAMOND SEAL available?", ["Yes", "No"])
        loss_rate = st.number_input("Enter Loss Rate (bbl/hr):", min_value=0)
        volume_of_lcm_pill = st.number_input("Volume of LCM Pill Planned (bbl):", min_value=0.0)
        if st.button("Get Recommendation"):
            st.session_state['loss_rate'] = loss_rate
            st.session_state['diamond_seal_available'] = diamond_seal_available == "Yes"
            with st.spinner('Generating recommendations...'):
                time.sleep(2)  # Simulate a delay
                st.session_state['recommendation_list'] = stoppit_decision_tree(loss_rate, st.session_state['diamond_seal_available'])
                st.session_state['index'] = 0
                primary_recommendations, _ = st.session_state['recommendation_list']
                if primary_recommendations:
                    st.write("Primary Chemicals Recommendation:")
                    for rec in primary_recommendations:
                        rec['Standard Sack Size (kg)'] = lookup_standard_sack_size(rec['Chemical'])
                    df_primary = pd.DataFrame(primary_recommendations)
                    st.dataframe(df_primary)

    elif formation_type == "Formations requiring Acid solubility":
     loss_rate = st.number_input("Enter Loss Rate (bbl/hr):", min_value=0)
     if st.button("Get Recommendation"):
        st.session_state['loss_rate'] = loss_rate
        with st.spinner('Generating recommendations...'):
            time.sleep(2)  # Simulate a delay
            st.session_state['recommendation_list'] = barablend_657_decision_tree(loss_rate)
            st.session_state['index'] = 0
            primary_recommendations, _ = st.session_state['recommendation_list']
            if primary_recommendations:
                st.write("Primary Chemicals Recommendation:")
                for rec in primary_recommendations:
                    rec['Standard Sack Size (kg)'] = lookup_standard_sack_size(rec['Chemical'])
                df_primary = pd.DataFrame(primary_recommendations)
                st.dataframe(df_primary)

    elif formation_type == "Reservoir Zone":
     loss_rate = st.number_input("Enter Loss Rate (bbl/hr):", min_value=0)
     if st.button("Get Recommendation"):
        st.session_state['loss_rate'] = loss_rate
        with st.spinner('Generating recommendations...'):
            time.sleep(2)  # Simulate a delay
            primary_table, secondary_table = reservoir_decision_tree(loss_rate)
            if primary_table:
                st.write("Primary Chemicals Recommendation:")
                for rec in primary_table:
                    rec['Standard Sack Size (kg)'] = lookup_standard_sack_size(rec['Chemical'])
                df_primary = pd.DataFrame(primary_table)
                st.dataframe(df_primary)
            if secondary_table:
                st.write("Speciality Chemicals Recommendation:")
                for rec in secondary_table:
                    rec['Standard Sack Size (kg)'] = lookup_standard_sack_size(rec['Chemical'])
                df_secondary = pd.DataFrame(secondary_table)
                st.dataframe(df_secondary)

    elif formation_type == "Non-Reservoir Zone":
     loss_rate = st.number_input("Enter Loss Rate (bbl/hr):", min_value=0)
     if st.button("Get Recommendation"):
        st.session_state['loss_rate'] = loss_rate
        with st.spinner('Generating recommendations...'):
            time.sleep(2)  # Simulate a delay
            primary_table, secondary_table = non_reservoir_decision_tree(loss_rate)
            if primary_table:
                st.write("Primary Chemicals Recommendation:")
                for rec in primary_table:
                    rec['Standard Sack Size (kg)'] = lookup_standard_sack_size(rec['Chemical'])
                df_primary = pd.DataFrame(primary_table)
                st.dataframe(df_primary)
            if secondary_table:
                st.write("Speciality Chemicals Recommendation:")
                for rec in secondary_table:
                    rec['Standard Sack Size (kg)'] = lookup_standard_sack_size(rec['Chemical'])
                df_secondary = pd.DataFrame(secondary_table)
                st.dataframe(df_secondary)

    else:
     st.write("Please select a valid formation type.")

    st.header("Simple Calculator")

    # Simple calculator implementation
    st.subheader("Calculator")
    st.write("Perform simple arithmetic operations.")
    num1 = st.number_input("Number 1", value=0.0)
    num2 = st.number_input("Number 2", value=0.0)
    operation = st.selectbox("Select Operation", ["Add", "Subtract", "Multiply", "Divide"])
    
    if st.button("Calculate"):
        if operation == "Add":
            result = num1 + num2
        elif operation == "Subtract":
            result = num1 - num2
        elif operation == "Multiply":
            result = num1 * num2
        elif operation == "Divide":
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Error: Division by zero"
        st.write(f"Result: {result}")

if __name__ == "__main__":
    main()
