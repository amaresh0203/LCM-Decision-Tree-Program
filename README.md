# Lost Circulation Treatment Program

This Streamlit app provides a decision-making tool for lost circulation treatments in drilling operations. The app uses predefined decision trees to recommend suitable chemical treatments based on the loss rate of drilling fluid. It offers treatment suggestions for both reservoir and non-reservoir zones and supports multiple scenarios.
For the input data I have used Halliburton Loss Circu;ation Decision Trees and reserves complete rights for the same.

The webapp has been deployed using streamlit cloud services that can be accessed with this link: https://lcm-decision-tree-program-2.streamlit.app/
## Features
- **Decision Trees for Different Scenarios**: The app includes decision trees for different loss rate scenarios, such as `stoppit`, `barablend-657`, `non-reservoir`, and `reservoir` decision trees.
- **Dynamic Recommendations**: Provides dynamic chemical treatment recommendations based on user input.
- **Visualizations**: Generates bar charts to visualize the concentration of recommended chemicals.
- **Data Export**: Allows users to download the recommendations as a CSV file.

Usage
- Enter the loss rate in the input field.
- Select the zone type (reservoir or non-reservoir) for the decision tree to use.
- Choose any specific conditions, such as the availability of certain chemicals.
- The app will display a table with treatment recommendations and a bar chart visualizing the concentrations of each chemical.
- Download the recommendations as a CSV file if needed.
- Decision Trees

The app includes to suggest recommendations for the following zones:
- "Permeable Sandstone type of formations"
- "Reservoir Zone",
- "Non-Reservoir Zone",
- "Formations requiring Acid solubility

Data
The app uses a predefined set of standard sack sizes for different chemicals to calculate the necessary amounts for each treatment. These values are stored in a dictionary within the app code.

Acknowledgements
- Special thanks to Halliburton for providing the Loss Circulation Decision Trees that form the basis of this app. All rights to these decision trees and chemicals are reserved by Halliburton.
- Streamlit for providing a simple and effective platform for building web apps.
- Plotly for the visualizations.
