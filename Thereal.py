#This file contains the logic for the study session as well as the information saved into the json file

import time
from datetime import datetime
import hardware as hw
import json
import os

session_ended = False
user_total_points = 0 #total point the user has(the start)
session_history = [] #stores every completed session
current_session_active = False #tells if the session is running
#user performace for session
selected_week = None
start_time = 0 #the start of the session
current_points = 0 #how many points user has during session
current_violations = 0 #how many violations user has during the session
remaining_seconds = 0 #for the countdown timer
grace_start_time = 0 #start time for grace period
grace_violation = False #tells if the grace 5sec has been used or not
violation_lock = False #makes sure the violation doesn't spam
break_interval_sec = 900 #breaks every 15 mins
break_duration_sec = 300 #gives a 5 min break
on_break = False #tells if user is in break mode
break_time_remaining = 0 #shows time left for brek
last_break_time = 0 #when the last break is 
store_giftcards = [{"name": "$5 Starbucks Gift Card",  "cost": 300},
    {"name": "$10 Ross Gift Card",       "cost": 500},
    {"name": "$10 DoorDash Gift Card",   "cost": 500},
    {"name": "$10 Apple Gift Card",       "cost": 800},
    {"name": "$10 Visa Gift Card",       "cost": 10},
    {"name": "$10 FREE GIFT CARD (Demo)",       "cost": 0}] #giftcards***fill this in
purchased_giftcards = [] #stores bought giftcards in list
buzzer_active = False #tells if the buzzer needs to make a sound or not
led_active = False #tells if led is blinking
last_buzz_time = 0 #last time the buzzer buzz for the session
start_distance = 0 #start distance for set up
tolerance = 2.0 #being able to move around
total_session_sec = 0 #shows the time left
session_status = "Ready to start"

# the set up     
def start_session(minutes):
    global current_session_active, start_time, total_session_sec
    global current_points, current_violations, remaining_seconds
    global grace_violation, violation_lock, on_break, start_distance
    global break_time_remaining, last_break_time, grace_start_time, user_total_points
    
    session_ended = False
    current_session_active = True
    start_time = time.time()
    total_session_sec = minutes*60
    remaining_seconds = total_session_sec
    current_points = minutes*5
    current_violations = 0
    grace_violation = False
    grace_start_time = 0
    violation_lock = False
    on_break = False
    break_time_remaining = 0
    last_break_time = start_time
    print("Session has started")
    
    #hardware
    #gets the distance
    start_distance = hw.get_distance() 
    hw.green_on() #turn green on when start session
    print(f"Session started. Baseline distance: {start_distance} cm")

#the countdown timer
def update_timer():
    global remaining_seconds, total_session_sec, start_time, current_session_active
 
    #if the session is not going on do nothing
    if not current_session_active: 
        return
    #if the session is not running, stop it
    elapsed_time = time.time() - start_time #time gone by
    remaining_seconds = int(total_session_sec - elapsed_time) #time shown to user
    # getting the distance from hardware file
    current_dist = hw.get_distance()
    handle_violation(current_dist) # Check if phone was moved
    #condition: if they hit 0 sec, green light turn off, buzzer goes off and session ends
    if remaining_seconds <= 0:
        hw.green_off()
        hw.buzz(0.5) # Notify session end
        end_session()

        
def handle_violation(distance):
    global current_points, current_violations, session_status
    global grace_violation, violation_lock, grace_start_time
    
    #no violation if the phone is still on stand (with in tolerance)
    if abs(distance - start_distance) <= tolerance:
        #after you use pick up the phone the first time, True=used violation, grace period is used
        if grace_start_time > 0:
            grace_violation = True
            session_status = "Grace period used up because phone was moved."
        grace_start_time = 0
        #else this is what happens if phone in good distance
        violation_lock = False
        hw.green_on()
        hw.red_off()
        session_status = "Phone on stand"
        return
    # If phone is moved:
    hw.green_off()
    hw.red_on() # Alert user visually
    
    #grace period------------------
    #the first time moving start the 5 sec timer
    if not grace_violation:
        #if you have not use the grace start the time
        if grace_start_time == 0:
            #start timer
            grace_start_time = time.time()
            session_status = "First pickup detected: Grace period started (One-time only)."
        #checking the 5 sec timer
        if time.time() - grace_start_time >= 5:
            #after 5secs is up start taking points
            current_points -= 1
            if not violation_lock:
                #only one violation
                current_violations += 1
                violation_lock = True

            session_status = f"Violation Points: {current_points}"
            #now you have used the violation
            grace_violation = True
            hw.buzz(0.2) #warning beep
            session_status = f"Grace Period Over"
        
    else:
        #----after grace period is used up------
        #take away points instantly no more grace
        current_points -= 1
        if not violation_lock:
            current_violations += 1 #1 violation added
            violation_lock = True
        grace_violation = True
        hw.buzz(0.1)
        session_status = f"Points being Taken Away"
    #if points get to 0 then end the game
    if current_points <= 0:
        game_over()

#what happens when the game is over
def game_over():
    global current_session_active, session_status

    session_status ="Game Over - You lost all points"
    hw.buzz(3) #buzzer goes off
    # reset or end session safely
    end_session() # end session

#print updated points
def update_points():
    global current_points
    print(f"Points: {current_points}")

#summary to be add to the history
def end_session():
    global current_session_active, user_total_points,current_points, session_ended
    
    if session_ended:
        return
    session_ended = True #session ended
    current_session_active = False #stops the session
    user_total_points += current_points #update and save the points
    d = datetime.now()
    #session aspects 
    session_record = {
        "time": d.strftime("%Y-%m-%d %I:%M:%S %p"),
        "year": d.year,
        "month": d.month,
        "week": str(d.date()),
        "points_earned": current_points,
        "violations": current_violations,
        "session_length_minutes": total_session_sec // 60,
        "final_score": current_points
    }
    session_history.append(session_record) #save it to the history
    save_points() #save the points
    show_summary() #show it in the summary

#summay screen
def show_summary():
    global current_points,current_violations
    print("Session complete")
    print(f"Points:{current_points}")
    print(f"Violations: {current_violations}")

#history screen
def show_history():
    print("---SESSION HISTORY---")
    
    count = 1
    for session in session_history:
        print(f"\nSession {count}")
        print(f"Time: {session['time']}")
        print(f"Minutes: {session['session_length_minutes']}")
        print(f"Points: {session['points_earned']}")
        print(f"Violations: {session['violations']}")
        count += 1 #add another session

#store
def show_store():
    print("\n---Store---")
    i = 1
    #add on the new giftcards
    for item in store_giftcards:
        print(i, ".", item["name"], "-", item["cost"], "points")
        i = i + 1
        
        print(f"\n Your Points: {user_total_points}")

    
SAVE_FILE = "studysense_data.json"
def save_points():
    """Save total points and session history to file."""
    # Convert date objects to strings so JSON can handle them
    safe_history = []
    for s in session_history:
        record = s.copy()
        record["week"] = str(record["week"])
        safe_history.append(record)
    
    data = {
        "total_points": user_total_points,
        "history": safe_history
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_points():
    """Load saved points and history when app starts."""
    global user_total_points, session_history
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            data = json.load(f)
            user_total_points = data.get("total_points", 0)
            session_history = data.get("history", [])
            purchased_giftcards = data.get("purchases", [])















