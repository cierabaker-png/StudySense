# StudySense
Interactive study session tracker built with Python and Kivy, integrating GPIO hardware and JSON-based data storage

Brief description of the project idea:

Phone distractions are one of the biggest barriers to productivity and focus, especially for students who struggle to stay off their devices during study sessions. Constant notifications and the habit of picking up your phone can break concentration and lead to poor academic performance. StudySense was created to tackle this problem by turning screen-free time into a rewarding experience. By gamifying self-discipline through a points-based reward system, StudySense motivates users to stay focused and build healthier habits over time. This helps students take control of their attention and perform at their best.

StudySense User Manual:


1. System Setup
This system can run without hardware. If you choose not the use hardware your keyboard will act as your phone interacting with the sensor.
"n" is used for putting your phone back while "f" is used for taking your phone away from the stand.


Hardware Setup (if using physical components):

Connect ultrasonic sensor:

• TRIG → GPIO 18

• ECHO → GPIO 27

Connect LEDs:

• Red LED → GPIO 16

• Green LED → GPIO 17

Connect buzzer:

• Buzzer → GPIO 22

Power on the Raspberry Pi.

Software Setup:

• Install required Python libraries:

• kivy

• pynput

• RPi.GPIO (only if using real hardware)

Place the following files in the same directory:

• hardware.py

• Thereal.py

• main2.py



2. Running the Application

• Open a terminal or command prompt.

• Navigate to the project folder.

• Run the program using:
python main2.py

• The graphical interface will launch.



3. Using the Application

Step 1: Start a Session

• From the Home Screen, click “Start Session.”

• Select a preset study time or enter a custom time.



Step 2: Session Initialization

• The system records the starting distance of the phone (baseline).

• The green LED turns on, indicating the session is active.



Step 3: During the Session

• Keep your phone in place to maintain points.

• The system continuously checks the distance:

• If the phone stays within range → no penalty

• If the phone moves beyond tolerance → violation triggered



Step 4: Violations

• A 5-second grace period is given on the first movement.

• After the grace period:

• Points are deducted

• Red LED turns on

• Buzzer provides feedback

• Additional movements result in immediate penalties.




Step 5: Session Completion

• When the timer reaches zero:

• The session ends automatically

• Points are awarded based on performance

• A summary screen is displayed



Optional: End Early

• The user can end the session early using the “End Session Early” button.

• Ending early results in zero points earned.



4. Simulation Mode (No Hardware)

• If hardware is not connected, the program runs in simulation mode.

• Use keyboard controls:

• Press “f” to simulate moving the phone away

• Press “n” to simulate placing the phone back

• The system behaves the same as with real hardware.



5. Viewing Progress

History Screen:

• View past sessions organized by month and week.

• See total points and violations per session.


Summary Screen:

• Displays:

• Time studied

• Points earned

• Violations

• Total points balance




6. Store System

• Access the Store from the Home Screen.

• View available rewards (gift cards).

• Select an item to purchase:

• If enough points are available → purchase is completed

• Points are deducted and saved

• Purchases are stored in history.



7. Data Storage

• All user data is saved locally in a JSON file:

• Total points

• Session history

• Purchases

• Data is automatically loaded when the application starts.




8. Ending the Application

• Close the application window to exit.

• If using real hardware, GPIO pins are automatically cleaned up.

interaction.



