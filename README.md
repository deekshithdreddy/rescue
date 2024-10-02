# EvacuAid Hub

[//]: # ([![EvacuAid Demo]&#40;images/evacuaid_banner.png&#41;]&#40;https://www.youtube.com/watch?v=zYok-lRehNQ&#41; )


[<img src="images/evacuaid_banner.png" width="50%">](https://www.youtube.com/watch?v=zYok-lRehNQ "Evacuaid Demo")

This was created for my project submission to the [MLH Month Long Hackathon November 2023](https://hackfest-november.devpost.com/)

## Overview

EvacuAid Hub is a Streamlit app developed to enhance disaster management efforts, 
especially in areas prone to frequent typhoons and disasters like the Philippines.
The app focuses on optimizing aid distribution during disasters, 
allowing evacuation sites to specify their inventory needs publicly and
enabling the public to view and respond to these needs. It also allows admin users 
to create reports and an inventory internally for monitoring purposes.

## Demo live Site
To demo live site: [click here](https://evacuaid-demo.streamlit.app/)
- Context:
- The app was modeled from the Philippine context and based on
the local [Disaster Response Operations Monitoring and Information Center (DROMIC)](https://dromic.dswd.gov.ph/)
reporting system, however it can be adapted to other reporting systems or practices.
- Schools in the Philippines are often used as evacuation centers,
so the demo site mainly has schools listed as the evacuation sites.
- To try the demo admin login with dummy credentials:
```
username = "public_user" 
password = "123evacuaid"
```
- I currently have two repos, I had to recreate it for deploying to streamlit,
 the other repo can be accessed here: [Evacuaid Deploy](https://github.com/Mikerniker/Evacuaid_demo) 

## Features

- **Public View:**
  - Interactive map showcasing evacuation sites and their specific inventory needs.
  - Accessible contact details for donation coordination.
  - Chatbot functionality for user inquiries.

- **Internal Admin View:**
  - Situation Reports page for creating and saving detailed reports.
  - Inventory Database to manage site-specific inventory data.
  - Report Records page for comprehensive access to all reports and inventories.

## How to Use

1. Clone the repository:

   ```
   bash
   git clone https://github.com/your-username/evacuaid.git
   ```

2. Install dependencies:

```pip install -r requirements.txt```


3. Run the app:
```streamlit run Home.py```

## Future Improvements
- Enhance chatbot to make it more user-friendly or interactive.
- Address glitches and improve authentication security.
- Implement a better user login/password/register options.
- Allow users to modify or update the inventory database.
- Refine functionality based on actual processes.
- Organize and fix code to make it cleaner

Feel free to clone the repository, explore the code!

Thank you for visiting!