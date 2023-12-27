# Gateway Discord Bot Source Code
Gateway, originally conceived as a versatile bot by Indie HQ, encountered discontinuation due to a decline in developer interest, ultimately leading to its closure.

## Deployment Instructions

**Install Requirements:**
`pip install -r requirements.txt`

**Token Configuration:**
Insert your token in "main.py" at line 643.

**API Keys:**
Ensure you possess API keys for:
- `OpenAI`- `Line- 28 At cogs/general.py`
- `Google` - `Line 29 At cogs/general.py`
- `Google API CX` - `Line 30 At cogs/general.py`
- `Spotify`- `Idk, find it out`

**Database Setup:**
Create an SQLite database by navigating to the "database" folder and executing the SQL script:
`sqlite3 -init database.sql`
>create an portgress sql db and put the connection like in main.py - line 379

   
Make sure to adjust the database path in the code to match your setup.

**PostgreSQL Connection:**
If you prefer PostgreSQL, set up a connection using services like Elephant SQL or Supabase. Modify the code accordingly and create an event for the database connection.

**Event Handling:**
Create the necessary database tables and events by running "database.py" located in a separate directory after its creation.

**Update Cogs:**
Adjust the cogs folders to ensure the code works correctly on your machine. Inspect and update paths in the code to match your local environment.

**Run the Project:**
`python main.py`

### Important Notes
**Educational Purpose Only:**
This source code is strictly intended for educational purposes. Any use for skidding or unauthorized activities is strictly prohibited.

**Permissions:**
No copies or reproductions of this code should run without explicit permission from the actual owners of this repository and Team Indie.

**Extended Features:**
Explore additional functionalities, such as ticket transcript and Chat Exporter, by following the setup instructions for the domain.

**Contribution Guidelines:**
Feel free to contribute to the project by submitting pull requests. Refer to the contributing guidelines for more details.

**Community Support:**
Join our vibrant community forum or reach out to Team Indie for assistance, discussions, and collaborative opportunities.

Special Thanks To Contributors/Developers
@Nova @Zeck @Anay @DREXYOP
`( Happy Skidding! )` 
> Learn to code bruh



*Note*: The commitment to open-source values and the promotion of learning remain at the core of this initiative. Let's build and learn together! 🚀
Any kind of usage of this repo should include proper credits to the original repo and its developers .
