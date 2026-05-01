#Header
#Project title: StudySense
#Team name: Group 31
#Team members: Ciera Baker, Aleena Peter, Oluwagbemiga Akinsola
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from Thereal import start_session
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from datetime import datetime, timedelta
import Thereal
import json
import os
Config.set('kivy', 'log_level', 'debug') #only puts what it needs to 
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
] #months for the history
# ── Color Palette ──────────────────────────────────────────────────────
NAVY   = (0, 0, 0.65, 1)   # dark navy - main background
NAVY2  = (0.08, 0.15, 0.35, 1)   # slightly lighter navy 
BLUE   = (0.15, 0.35, 0.75, 1)   # bright blue 
WHITE  = (0.95, 0.95, 0.95, 1)   # off-white 
BLACK  = (0.05, 0.05, 0.08, 1)   # near black 
GOLD   = (0.72, 0.53, 0.04, 1)   # gold 
RED    = (0.90, 0.20, 0.25, 1)   # red 

#kwargs = can add more parameters if need to 
#function for styling each button 
def styled_btn(text, bg=None, font_size=16, **kwargs):
    #Returns a consistently styled Button
    return Button(
        text=text,
        background_color=list(bg or BLUE),
        color=list(WHITE),
        font_size=font_size,
        bold=False,
        **kwargs
    )

#function for styling each label (text) that is made
def styled_label(text, size=16, color=None, **kwargs):
    #Returns a consistently styled Label
    return Label(
        text=text,
        font_size=size,
        color=list(color or WHITE),
        markup=True,
        **kwargs
    )

#What is shown on the Homescreen (first screen when program runs)        
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)#parent is screen (using screenmanager)
        #creating the screen
        layout = BoxLayout(orientation="vertical", spacing=15, padding=10)
        #this creates a white background
        with layout.canvas.before:
            Color(*WHITE)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        #this is so the program can resize
        layout.bind(size=lambda *a: setattr(self.rect, 'size', layout.size),
            pos=lambda *a: setattr(self.rect, 'pos', layout.pos))
        
        #color and size of StudySense
        title = Label(
            text="[color=000000]Study[color=3366cc]Sense[/color]",
            font_size=42, bold=True,
            markup=True,
            size_hint=(1, 0.3)
        )
        #color and size of Focus Earn Reward
        subtitle = Label(
            text="Focus. Earn. Reward.",
            font_size=14, color=(0, 0, 0, 1),
            size_hint=(1, 0.1)
        )
        # creating a button with color and size of start session
        start_button = Button(
            text="Start Session",
            size_hint=(1, 0.15),
            background_color=BLUE,
            color=WHITE, font_size=18, bold=True
        )
        #when press the start button go to timeselection screen
        start_button.bind(on_press=self.go_to_time)
        
        # creating a button with color and size of store button
        store_btn = Button(
            text="  Store",
            size_hint=(1, 0.15),
            background_color=NAVY2,
            color=WHITE, font_size=17
        )
        #when press store button go to store screen
        store_btn.bind(on_press=self.go_to_store)
        
        #creating a button with color and size of history button
        history_btn = Button(
            text="History",
            size_hint=(1, 0.15),
            background_color=NAVY2,
            color=WHITE, font_size=17
        )
        #when press hisory go to history screen
        history_btn.bind(on_press=self.go_to_history)
        
        #the order they appear on screen
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start_button)
        layout.add_widget(store_btn)
        layout.add_widget(history_btn)
        #make them visable on the screen
        self.add_widget(layout)
    #function to go to time selection screen
    def go_to_time(self, instance):
        self.manager.current = "time_select"
    #function to go to store screen
    def go_to_store(self, instance):
        self.manager.current = "store"
    #function to go to history screen
    def go_to_history(self, instance):
        self.manager.current = "history"

#Time Selecting screen 
class TimeSelectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) #parent is screen (using screenmanager)
        #creating a white background
        with self.canvas.before:
            Color(*WHITE)
            self._bg = Rectangle(size=self.size, pos=self.pos)
        #helps the screen resize properly
        self.bind(
            size=lambda *a: setattr(self._bg, 'size', self.size),
            pos=lambda *a:  setattr(self._bg, 'pos',  self.pos)
        )
        #creates the screen
        layout = BoxLayout(orientation='vertical', padding=[20, 30, 20, 20],
                         spacing=14)
        
        #creates the size and color of the header "Select Study Time"
        header = BoxLayout(size_hint_y=None, height=50)
        header.add_widget(styled_label("Select Study Time", color= (0,0,0,1), size=28))
        layout.add_widget(header)
        
        #creates the size and color of the subheader "More time = more points"
        layout.add_widget(styled_label(
            "More time = more points",
            size=17, color=(0.5, 0.6, 0.8, 1)
        ))
        
        #The list of preset times 
        presets = [25, 50, 90, 120]
        #loop through the preset list
        for mins in presets:
            #calls the function to make one for each number in list
            card = self._make_card(mins)
            layout.add_widget(card) #adds the button to the layout

        # creates and style the custom time text 
        layout.add_widget(styled_label("----- or enter custom -----", size=17, color=(0.5, 0.6, 0.8, 1)))
        #make the row that is for user input
        custom_row = BoxLayout(size_hint_y=None, height=50, spacing=10)
        #creates custom row with user input, color, size
        self.custom_input = TextInput(
            hint_text="Minutes (e.g. 40)", #what to have when there is not input
            multiline=False, #one line
            input_filter='int', #make sure that user only put an integer number
            size_hint_x=0.5,
            background_color=list(NAVY2),
            foreground_color=list(WHITE),
            hint_text_color=[0.5, 0.6, 0.8, 1], 
            cursor_color=list(WHITE),
            font_size=16
        )
        #creates a start button for user to click once entered time
        custom_btn = styled_btn("Start", font_size=15, size_hint_x=0.5)
        #onced clicked start go to session screen for custom inputs
        custom_btn.bind(on_press=self.start_custom_session)
        #add start and input buttons
        custom_row.add_widget(self.custom_input)
        custom_row.add_widget(custom_btn)
        #add to layout
        layout.add_widget(custom_row)
        self.add_widget(layout)
        #adding a back button and directing it back to the homescreen
        back = styled_btn(" Home", bg=NAVY2)
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back)
        
   #creatinng a button for each preset time     
    def _make_card(self, mins):
        pts = mins * 5 # 5 points for each minute
        # creating the card, acts as the button 
        card = BoxLayout(orientation='vertical', spacing=2,
                padding=[18, 10], size_hint_y=None, height=72)

        # Navy card background
        def draw(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(*NAVY2)
                Rectangle(pos=inst.pos, size=inst.size)
        #helps when resizing 
        card.bind(pos=draw, size=draw)
        #making a horizontal row for the text 
        top_row = BoxLayout(size_hint_y=None, height=30)
        #creating text for the minutes in row
        top_row.add_widget(styled_label(f"[b]{mins} minutes[/b]",
                                        size=20, halign='center', valign="middle"))
        #creating text for the points in row
        top_row.add_widget(styled_label(f"[color=ffd034] {pts} pts max[/color]",
                                        size=18, halign='center', valign="middle"))
        #adding the text to the card (button)
        card.add_widget(top_row)


        # making the card able to act like a button (click able)
        def on_touch(inst, touch):
            #if click on the actual button go to the session for that preset time
            if inst.collide_point(*touch.pos):
                self.start_session(mins)
                return True
            return False
        
        #connet to the on_touch function 
        card.bind(on_touch_down=on_touch)
        return card #sends to the layout
    
    #start session function to go to session screen
    def start_session(self, minutes):
        start_session(minutes)
        self.manager.current = "session"
    #start session function to go to custom session screen
    def start_custom_session(self, instance):
        text = self.custom_input.text
        #make sure text is a whole number
        if text.isdigit():
            self.start_session(int(text))
        else:
            self.custom_input.hint_text = "Enter a valid number!"

    #for the back button it will direct home
    def go_home(self, instance):
        self.manager.current = 'home'
   
#Session Screen (where everything runs)
class SessionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #creating a background
        with self.canvas.before:
            Color(0.94, 0.95, 0.98, 1)  # light blue-grey background #f0f3fa
            self._bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(
            size=lambda *a: setattr(self._bg, 'size', self.size),
            pos=lambda *a:  setattr(self._bg, 'pos',  self.pos)
        )
        #creates the layout for screen
        layout = BoxLayout(orientation='vertical', padding=[18, 22, 18, 22], spacing=11)

        #creating the title of the Study Sense
        top = BoxLayout(size_hint_y=None, height=36, spacing=10)
        top.add_widget(Label(
            text="[color=000000]Study[color=3366cc]Sense[/color]", font_size=20, markup=True,
            bold=True, halign='center',
            size_hint_y=None, height=36
        ))
        layout.add_widget(top)

        # creating the timer
        hero = BoxLayout(
            orientation='vertical',
            size_hint_y=None, height=130,
            padding=[14, 16]
        )
        #the box for the timer
        def draw_hero(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(0, 0, 0.55, 1)  # navy #00008c
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[20])
        hero.bind(pos=draw_hero, size=draw_hero)
        
        #making the timer text
        self.timer_label = Label(
            text="00:00", font_size=48,
            bold=True, color=(1, 1, 1, 1),
            size_hint_y=0.75
        )
        #the text of the "remaining" part of the timer
        hero.add_widget(self.timer_label)
        hero.add_widget(Label(
            text="remaining", font_size=11,
            color=(1, 1, 1, 0.5), size_hint_y=0.25
        ))
        layout.add_widget(hero)

        #creating the progress bar and styling it
        prog_wrap = BoxLayout(orientation='vertical', size_hint_y=None, height=28, spacing=4)
        prog_top = BoxLayout(size_hint_y=None, height=14)
        prog_top.add_widget(Label(
            text="session progress", font_size=11,
            color=(0.33, 0.33, 0.33, 1), halign='left'
        ))
        
        self.prog_pct_label = Label(
            text="0%", font_size=11,
            color=(0.33, 0.33, 0.33, 1), halign='right'
        )
        prog_top.add_widget(self.prog_pct_label)
        prog_wrap.add_widget(prog_top)

        # tracking the time 
        track = BoxLayout(size_hint_y=None, height=7)
        def draw_track(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(0.85, 0.87, 0.94, 1)  # #d8ddf0
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[4])
        track.bind(pos=draw_track, size=draw_track)

        self.prog_fill = Widget(size_hint_x=0)
        
        def draw_fill(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(0, 0, 0.55, 1)
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[4])
        self.prog_fill.bind(pos=draw_fill, size=draw_fill)
        track.add_widget(self.prog_fill)
        track.add_widget(Widget())  # remaining unfilled space
        prog_wrap.add_widget(track)
        layout.add_widget(prog_wrap)

        # creating points and violations cards 
        cards = BoxLayout(size_hint_y=None, height=80, spacing=10)

        def make_card(bg=(1, 1, 1, 1), border=(0.82, 0.84, 0.91, 1)):
            card = BoxLayout(orientation='vertical', padding=[14, 11])
            def draw_card(inst, *_):
                inst.canvas.before.clear()
                with inst.canvas.before:
                    Color(*border)
                    RoundedRectangle(pos=inst.pos, size=inst.size, radius=[14])
                    Color(*bg)
                    RoundedRectangle(
                        pos=(inst.pos[0] + 0.5, inst.pos[1] + 0.5),
                        size=(inst.size[0] - 1, inst.size[1] - 1),
                        radius=[14]
                    )
            card.bind(pos=draw_card, size=draw_card)
            return card

        pts_card = make_card()
        pts_card.add_widget(Label(text="POINTS", font_size=10,
                                   color=(0.53, 0.53, 0.53, 1), halign='left'))
        self.points_label = Label(text="0", font_size=26,
                                   bold=True, color=(0, 0, 0.55, 1), halign='left')
        pts_card.add_widget(self.points_label)
        cards.add_widget(pts_card)

        viol_card = make_card()
        viol_card.add_widget(Label(text="VIOLATIONS", font_size=10,
                                    color=(0.53, 0.53, 0.53, 1), halign='left'))
        self.violations_label = Label(text="0", font_size=26,
                                       bold=True, color=(0.69, 0.13, 0.13, 1), halign='left')
        viol_card.add_widget(self.violations_label)
        cards.add_widget(viol_card)

        layout.add_widget(cards)

        # ── Status chip ───────────────────────────────────────────────
        self.status_bar = BoxLayout(
            size_hint_y=None, height=46,
            padding=[13, 0], spacing=8
        )
        def draw_status(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(0.84, 0.94, 0.84, 1)  # green chip #d6f0d6
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[12])
        self.status_bar.bind(pos=draw_status, size=draw_status)
        self._status_draw = draw_status

        self.status_dot = Widget(size_hint_x=None, width=9)
        def draw_dot(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(0.16, 0.54, 0.16, 1)  # green dot
                Ellipse(
                    pos=(inst.center_x - 4.5, inst.center_y - 4.5),
                    size=(9, 9)
                )
        self.status_dot.bind(pos=draw_dot, size=draw_dot)
        self._dot_draw = draw_dot

        self.status_label = Label(
            text="Phone on stand — keep it up!",
            font_size=12, color=(0.1, 0.41, 0.1, 1), halign='left'
        )
        self.status_bar.add_widget(self.status_dot)
        self.status_bar.add_widget(self.status_label)
        layout.add_widget(self.status_bar)

        # ── Violation warning ─────────────────────────────────────────
        self.warn_label = Label(
            text="", font_size=12,
            color=(0.69, 0.13, 0.13, 1),
            size_hint_y=None, height=16
        )
        layout.add_widget(self.warn_label)

        layout.add_widget(Widget())  # spacer

        # ── End early button ──────────────────────────────────────────
        end_btn = Button(
            text="End Session Early",
            size_hint_y=None, height=50,
            background_normal='',
            background_color=(0, 0, 0.55, 1),
            color=(1, 1, 1, 1), font_size=14,
            bold=True
        )
        # Remove hover/ripple effect by disabling default background changes
        end_btn.background_down = ''
        end_btn.bind(on_press=self.end_early)
        layout.add_widget(end_btn)

        self.add_widget(layout)

    def on_enter(self):
        self.timer_label.text = "00:00"
        self.warn_label.text = ""
        Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        import Thereal
        Thereal.update_timer()

        rem    = Thereal.remaining_seconds
        pts    = Thereal.current_points
        viols  = Thereal.current_violations
        status = Thereal.session_status
        total  = Thereal.total_session_sec  # make sure this exists in Thereal

        m, s = divmod(max(rem, 0), 60)
        self.timer_label.text      = f"{m:02d}:{s:02d}"
        self.points_label.text     = str(pts)
        self.violations_label.text = str(viols)

        # Progress bar
        if total > 0:
            pct = max(0, min(1, (total - rem) / total))
            self.prog_fill.size_hint_x = pct
            self.prog_pct_label.text = f"{int(pct * 100)}%"

        # Status chip colour + dot + text
        def redraw_status(bg_color, dot_color, text, text_color):
            self.status_bar.canvas.before.clear()
            with self.status_bar.canvas.before:
                Color(*bg_color)
                RoundedRectangle(
                    pos=self.status_bar.pos,
                    size=self.status_bar.size,
                    radius=[12]
                )
            self.status_dot.canvas.before.clear()
            with self.status_dot.canvas.before:
                Color(*dot_color)
                Ellipse(
                    pos=(self.status_dot.center_x - 4.5,
                         self.status_dot.center_y - 4.5),
                    size=(9, 9)
                )
            self.status_label.text  = text
            self.status_label.color = text_color

        if "Grace" in status:
            redraw_status(
                (1, 0.96, 0.84, 1),        # yellow chip
                (0.78, 0.47, 0, 1),         # yellow dot
                "Grace period — put phone down now!",
                (0.47, 0.31, 0, 1)
            )
            self.warn_label.text = ""
        elif "Violation" in status or "Points" in status:
            redraw_status(
                (0.99, 0.91, 0.91, 1),     # red chip
                (0.72, 0.13, 0.13, 1),      # red dot
                "Phone picked up — put it down!",
                (0.6, 0.08, 0.08, 1)
            )
            self.warn_label.text = f"-1 point deducted  •  {pts} pts remaining"
        else:
            redraw_status(
                (0.84, 0.94, 0.84, 1),     # green chip
                (0.16, 0.54, 0.16, 1),      # green dot
                "Phone on stand — keep it up!",
                (0.1, 0.41, 0.1, 1)
            )
            self.warn_label.text = ""

        if rem <= 0:
            Clock.unschedule(self.update)
            self._go_summary(ended_early=False)

    def end_early(self, instance):
        Clock.unschedule(self.update)
        import Thereal
        Thereal.current_points = 0
        self._go_summary(ended_early=True)

    def _go_summary(self, ended_early):
        import Thereal
        Thereal.end_session()
        s = self.manager.get_screen('summary')
        s.load_summary(ended_early)
        self.manager.current = 'summary'

    def on_leave(self):
        Clock.unschedule(self.update)
        import hardware as hw
        hw.red_off()
        hw.green_off()

class SummaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(
            size=lambda *a: setattr(self._bg, 'size', self.size),
            pos=lambda *a:  setattr(self._bg, 'pos',  self.pos)
        )

        self.root = BoxLayout(orientation='vertical',
                              padding=[20, 0, 20, 20], spacing=10)
        self.add_widget(self.root)

    def load_summary(self, ended_early):
        self.root.clear_widgets()
        import Thereal

        pts   = Thereal.current_points
        viols = Thereal.current_violations
        mins  = Thereal.total_session_sec // 60
        bank  = Thereal.user_total_points

        # ── Header ────────────────────────────────────────────────────
        header = BoxLayout(size_hint_y=None, height=110)

        def draw_hdr(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(0, 0, 0, 1) if ended_early else Color(0, 0, 0.55, 1)
                Rectangle(pos=inst.pos, size=inst.size)

        header.bind(pos=draw_hdr, size=draw_hdr)

        hdr_inner = BoxLayout(orientation='vertical', padding=[16, 12])
        if ended_early:
            hdr_inner.add_widget(Label(text="Session Ended Early",
                                        font_size=13, color=(0.6, 0.6, 0.6, 1)))
            hdr_inner.add_widget(Label(text="0 Points Earned",
                                        font_size=26, bold=True, color=(1, 1, 1, 1)))
            hdr_inner.add_widget(Label(
                text="Complete the full session to earn points",
                font_size=11, color=(0.5, 0.5, 0.5, 1)))
        else:
            hdr_inner.add_widget(Label(text="Session Complete!",
                                        font_size=13, color=(0.7, 0.8, 1, 1)))
            hdr_inner.add_widget(Label(text=f"{pts} Points Earned",
                                        font_size=26, bold=True, color=(1, 1, 1, 1)))
            hdr_inner.add_widget(Label(text="Great work — stay consistent!",
                                        font_size=11, color=(0.6, 0.7, 0.9, 1)))

        header.add_widget(hdr_inner)
        self.root.add_widget(header)

        # ── Stat rows ─────────────────────────────────────────────────
        stats = [
            ("Time Studied",      f"{mins} min",  False),
            ("Points Earned",     str(pts),        ended_early),
            ("Violations",        str(viols),      viols > 0),
            ("Total Points Bank", str(bank),       False),
        ]

        for label_text, value, is_red in stats:
            row = BoxLayout(size_hint_y=None, height=54, padding=[16, 8])

            def draw_row(inst, *_):
                inst.canvas.before.clear()
                with inst.canvas.before:
                    Color(0.94, 0.96, 0.98, 1)
                    Rectangle(pos=inst.pos, size=inst.size)

            row.bind(pos=draw_row, size=draw_row)
            row.add_widget(Label(text=label_text, font_size=13,
                                  color=(0.4, 0.4, 0.4, 1), halign='left'))
            val_color = (0.75, 0.15, 0.15, 1) if is_red else (0, 0, 0.55, 1)
            row.add_widget(Label(text=value, font_size=18,
                                  bold=True, color=val_color, halign='right'))
            self.root.add_widget(row)
            self.root.add_widget(Widget(size_hint_y=None, height=6))

        self.root.add_widget(Widget())

        # ── Buttons ───────────────────────────────────────────────────
        btn_row = BoxLayout(size_hint_y=None, height=50, spacing=10)

        home_btn = Button(
            text="Home",
            background_color=(0, 0, 0.55, 1),
            color=(1, 1, 1, 1), font_size=14
        )
        home_btn.bind(on_press=lambda _: setattr(self.manager, 'current', 'home'))

        second_btn = Button(
            text="Store" if not ended_early else "Try Again",
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0.55, 1), font_size=14
        )

        def second_action(_):
            self.manager.current = 'store' if not ended_early else 'time_select'

        second_btn.bind(on_press=second_action)

        btn_row.add_widget(home_btn)
        btn_row.add_widget(second_btn)
        self.root.add_widget(btn_row)



class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.94, 0.95, 0.98, 1)  # same light blue-grey as SessionScreen
            self._bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(
            size=lambda *a: setattr(self._bg, 'size', self.size),
            pos=lambda *a:  setattr(self._bg, 'pos',  self.pos)
        )

        root = BoxLayout(orientation='vertical', padding=[18, 22, 18, 22], spacing=12)

        # ── Title ─────────────────────────────────────────────────────
        root.add_widget(Label(
            text="History", font_size=22,
            bold=True, color=(0, 0, 0.55, 1),
            halign='center', size_hint_y=None, height=36
        ))

        # ── Month picker row ──────────────────────────────────────────
        picker_label = Label(
            text="Select a month:", font_size=12,
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None, height=24, halign='left'
        )
        root.add_widget(picker_label)

        # Two rows of 6 months each
        self._selected_month = datetime.now().month  # default to current month
        self._month_btns = []

        for row_months in [MONTHS[:6], MONTHS[6:]]:
            row = BoxLayout(size_hint_y=None, height=36, spacing=6)
            for i, month_name in enumerate(row_months):
                month_num = MONTHS.index(month_name) + 1
                btn = Button(
                    text=month_name[:3],  # short name e.g. "Jan"
                    font_size=11,
                    background_normal='',
                    background_color=(0, 0, 0.55, 1) if month_num == self._selected_month else (0.88, 0.90, 0.96, 1),
                    color=(1, 1, 1, 1) if month_num == self._selected_month else (0, 0, 0.55, 1),
                )
                btn.bind(on_press=lambda x, m=month_num: self.select_month(m))
                self._month_btns.append((month_num, btn))
                row.add_widget(btn)
            root.add_widget(row)

        # ── Scrollable week list ──────────────────────────────────────
        scroll = ScrollView(size_hint=(1, 1))
        self.week_list = BoxLayout(
            orientation='vertical', spacing=10,
            size_hint_y=None, padding=[0, 8]
        )
        self.week_list.bind(minimum_height=self.week_list.setter('height'))
        scroll.add_widget(self.week_list)
        root.add_widget(scroll)

        # ── Back button ───────────────────────────────────────────────
        back_btn = Button(
            text="Back",
            size_hint_y=None, height=44,
            background_normal='',
            background_color=(0, 0, 0.55, 1),
            color=(1, 1, 1, 1), font_size=13
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        root.add_widget(back_btn)

        self.add_widget(root)

    def on_pre_enter(self):
        self.load_month(self._selected_month)

    def select_month(self, month_num):
        self._selected_month = month_num
        # Update button styles
        for m, btn in self._month_btns:
            if m == month_num:
                btn.background_color = (0, 0, 0.55, 1)
                btn.color = (1, 1, 1, 1)
            else:
                btn.background_color = (0.88, 0.90, 0.96, 1)
                btn.color = (0, 0, 0.55, 1)
        self.load_month(month_num)

    def load_month(self, month_num):
        import Thereal
        self.week_list.clear_widgets()

        sessions = [
            s for s in Thereal.session_history
            if s["month"] == month_num
        ]

        if not sessions:
            self.week_list.add_widget(Label(
                text=f"No sessions recorded for {MONTHS[month_num - 1]}.",
                font_size=13, color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None, height=48
            ))
            return

        # Group by ISO week number
        weeks = {}
        for s in sessions:
            # s["week"] is stored as a date object or string — get ISO week
            week_num = s["week"]  # already 1, 2, 3, 4
            if week_num not in weeks:
                weeks[week_num] = []
            weeks[week_num].append(s)

        # Week-of-month label (1st week in month = Week 1, etc.)
        week_keys = sorted(weeks.keys())
        for display_num, week_key in enumerate(week_keys, start=1):
            items = weeks[week_key]
            total_pts = sum(s["points_earned"] for s in items)
            total_viol = sum(s["violations"] for s in items)

            # Card container
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None, height=72,
                padding=[14, 10]
            )
            def draw_card(inst, *_, wk=display_num):
                inst.canvas.before.clear()
                with inst.canvas.before:
                    Color(1, 1, 1, 1)
                    RoundedRectangle(pos=inst.pos, size=inst.size, radius=[12])
                    # Left blue accent border
                    Color(0, 0, 0.55, 1)
                    RoundedRectangle(
                        pos=inst.pos,
                        size=(4, inst.size[1]),
                        radius=[2]
                    )
            card.bind(pos=draw_card, size=draw_card)

            top_row = BoxLayout(size_hint_y=0.55)
            top_row.add_widget(Label(
                text=f"Week {display_num}  •  {len(items)} session{'s' if len(items) != 1 else ''}",
                font_size=13, bold=True, color=(0, 0, 0.55, 1), halign='left'
            ))
            card.add_widget(top_row)

            bottom_row = BoxLayout(size_hint_y=0.45)
            bottom_row.add_widget(Label(
                text=f"{total_pts} pts  |  {total_viol} violations",
                font_size=11, color=(0.45, 0.45, 0.45, 1), halign='left'
            ))
            # Tap arrow
            bottom_row.add_widget(Label(
                text="›", font_size=20,
                color=(0, 0, 0.55, 1), halign='right'
            ))
            card.add_widget(bottom_row)

            # Make the whole card tappable
            card_btn = Button(
                size_hint=(1, None), height=72,
                background_normal='', background_color=(0, 0, 0, 0),
                opacity=0
            )
            card_btn.bind(on_press=lambda x, wk=week_key: self.open_week(wk))

            # Wrap card + invisible button in a FloatLayout
            wrapper = FloatLayout(size_hint_y=None, height=72)
            card.pos_hint = {'x': 0, 'y': 0}
            card.size_hint = (1, 1)
            wrapper.add_widget(card)
            card_btn.pos_hint = {'x': 0, 'y': 0}
            card_btn.size_hint = (1, 1)
            wrapper.add_widget(card_btn)

            self.week_list.add_widget(wrapper)

    def open_week(self, week_key):
        import Thereal
        Thereal.selected_week = week_key   # ← set FIRST, then navigate
        self.manager.current = "weeklyview"


class HistoryWeeklyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.94, 0.95, 0.98, 1)
            self._bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(
            size=lambda *a: setattr(self._bg, 'size', self.size),
            pos=lambda *a:  setattr(self._bg, 'pos',  self.pos)
        )

        root = BoxLayout(orientation='vertical', padding=[18, 22, 18, 22], spacing=12)

        # ── Header summary block ──────────────────────────────────────
        self.header = BoxLayout(
            orientation='vertical',
            size_hint_y=None, height=90,
            padding=[16, 12]
        )
        def draw_header(inst, *_):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(0, 0, 0.55, 1)
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[16])
        self.header.bind(pos=draw_header, size=draw_header)

        self.week_title = Label(
            text="Week —", font_size=16,
            bold=True, color=(1, 1, 1, 1),
            halign='left', size_hint_y=0.5
        )
        self.week_summary = Label(
            text="", font_size=12,
            color=(1, 1, 1, 0.65),
            halign='left', size_hint_y=0.5
        )
        self.header.add_widget(self.week_title)
        self.header.add_widget(self.week_summary)
        root.add_widget(self.header)

        # ── Scrollable session rows ───────────────────────────────────
        scroll = ScrollView(size_hint=(1, 1))
        self.session_list = BoxLayout(
            orientation='vertical', spacing=0,
            size_hint_y=None
        )
        self.session_list.bind(minimum_height=self.session_list.setter('height'))
        scroll.add_widget(self.session_list)
        root.add_widget(scroll)

        # ── Back button ───────────────────────────────────────────────
        back_btn = Button(
            text="← Back",
            size_hint_y=None, height=44,
            background_normal='',
            background_color=(0, 0, 0.55, 1),
            color=(1, 1, 1, 1), font_size=13
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'history'))
        root.add_widget(back_btn)

        self.add_widget(root)

    def on_pre_enter(self):
        import Thereal
        self.session_list.clear_widgets()

        week_key = Thereal.selected_week
        print(f"Looking for week: {week_key}, type: {type(week_key)}")
        print(f"Total sessions: {len(Thereal.session_history)}")
        sessions = [
            s for s in Thereal.session_history
            if s["week"] == week_key
        ]
                    # Header summary
        total_pts  = sum(s["points_earned"] for s in sessions)
        total_viol = sum(s["violations"] for s in sessions)
        self.week_title.text   = f"Week {week_key}"
        self.week_summary.text = f"{len(sessions)} sessions  •  {total_pts} pts total  •  {total_viol} violations"

        if not sessions:
            self.session_list.add_widget(Label(
                text="No sessions this week.",
                font_size=13, color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None, height=48
            ))
            return

        for i, s in enumerate(reversed(sessions)):
            row = BoxLayout(
                size_hint_y=None, height=58,
                padding=[14, 8]
            )
            is_last = (i == len(sessions) - 1)
            def draw_row(inst, *_, last=is_last):
                inst.canvas.before.clear()
                with inst.canvas.before:
                    Color(1, 1, 1, 1)
                    Rectangle(pos=inst.pos, size=inst.size)
                if not last:
                    with inst.canvas.after:
                        Color(0.88, 0.90, 0.96, 1)  # divider
                        Rectangle(
                            pos=(inst.pos[0] + 14, inst.pos[1]),
                            size=(inst.size[0] - 28, 1)
                        )
            row.bind(pos=draw_row, size=draw_row)

            left = BoxLayout(orientation='vertical', size_hint_x=0.7)
            left.add_widget(Label(
                text=s['time'], font_size=11,
                color=(0.3, 0.3, 0.3, 1), halign='left'
            ))
            #how long the session is 
            left.add_widget(Label(
                text=f"{s['session_length_minutes']} min session",
                font_size=11, color=(0.55, 0.55, 0.55, 1), halign='left'
            ))
            row.add_widget(left)
            #points earned text 
            right = BoxLayout(orientation='vertical', size_hint_x=0.3)
            right.add_widget(Label(
                text=f"{s['points_earned']} pts",
                font_size=13, bold=True,
                color=(0, 0, 0.55, 1), halign='right'
            ))
            #violations text 
            right.add_widget(Label(
                text=f"{s['violations']} viol.",
                font_size=11,
                color=(0.69, 0.13, 0.13, 1), halign='right'
            ))
            row.add_widget(right)

            self.session_list.add_widget(row)
#Store Screen 
class StoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #creat a white background
        with self.canvas.before:
            Color(*WHITE)
            self._bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(
            size=lambda *a: setattr(self._bg, 'size', self.size),
            pos=lambda *a:  setattr(self._bg, 'pos',  self.pos)
        )

        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)

        layout.add_widget(styled_label("Store", size=30, color=(0,0,0,1)))
        #show total points
        self.points_label = styled_label(
            f"Your Points: {Thereal.user_total_points}",
            size=18, color=(0,0,0,1)
        )
        layout.add_widget(self.points_label)

        #make each button for the giftcards
        for i, item in enumerate(Thereal.store_giftcards):
            btn = styled_btn(
                f"{item['name']}  —  {item['cost']} pts",
                
                
                font_size=15,
                size_hint_y=None, height=70
            )
            btn.bind(on_press=lambda x, idx=i: self.go_to_item(idx))
            layout.add_widget(btn)

        back = styled_btn(" Home", size_hint_y=None, height=50)
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back)

        self.add_widget(layout)

    def on_pre_enter(self):
        # Refresh points every time you visit the store
        self.points_label.text = f"Your Points: {Thereal.user_total_points}"

    def go_to_item(self, index):
        # Pass the selected item to ItemScreen then navigate
        item_screen = self.manager.get_screen('item')
        item_screen.load_item(Thereal.store_giftcards[index], index)
        self.manager.current = 'item'
        
class ItemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*WHITE)
            self._bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(
            size=lambda *a: setattr(self._bg, 'size', self.size),
            pos=lambda *a:  setattr(self._bg, 'pos',  self.pos)
        )

        layout = BoxLayout(orientation='vertical', padding=30, spacing=16)

        # These get filled in by load_item()


        self.buy_btn = styled_btn("Buy Now", bg=BLUE)
        self.buy_btn.bind(on_press=self.buy_item)

        back = styled_btn("Back to Store", bg=NAVY2)
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'store'))
        self.name_label = styled_label("", size=30, color= BLACK)
        self.cost_label = styled_label("", size=20, color= BLACK)
        self.pts_label  = styled_label("", size=18, color= BLACK)
        self.msg_label  = styled_label("", size=18, color= BLACK)
        
        layout.add_widget(self.name_label)
        layout.add_widget(self.cost_label)
        layout.add_widget(self.pts_label)
        layout.add_widget(self.msg_label)
        layout.add_widget(self.buy_btn)
        layout.add_widget(back)

        self.add_widget(layout)
        self._current_item = None

    def load_item(self, item, index):
        """Called by StoreScreen before navigating here."""
        self._item_index = index
        self.name_label.text  = f"[b]{item['name']}[/b]"
        self.cost_label.text  = f"Cost: {item['cost']} points"
        self.pts_label.text   = f"Your balance: {Thereal.user_total_points} pts"
        self.msg_label.text   = ""

        # Show or hide buy button based on whether they can afford it
        if Thereal.user_total_points >= item['cost']:
            self.buy_btn.disabled = False
            self.buy_btn.text = "Buy Now"
            self.buy_btn.background_color = list(BLUE)
        else:
            self.buy_btn.disabled = True
            self.buy_btn.text = " Not Enough Points"
            self.buy_btn.background_color = [0.3, 0.1, 0.1, 1]

    def buy_item(self, instance):

        if self._item_index is None:
            return

        item = Thereal.store_giftcards[self._item_index]
        # Check points directly here instead of relying on Thereal.buy_item
        if Thereal.user_total_points >= item['cost']:
            # Deduct points
            Thereal.user_total_points -= item['cost']
        
            # Add to purchased list
            Thereal.purchased_giftcards.append(item['name'])
        
            # Save to JSON file immediately
            Thereal.save_points()
            # Update display after purchase
            self.pts_label.text  = f"Your balance: {Thereal.user_total_points} pts"
            self.msg_label.color = list(GOLD)
            self.msg_label.text  = "Purchased! Keep studying!"
            self.buy_btn.disabled = True
            self.buy_btn.text = " Purchased"
            self.buy_btn.background_color = [0.1, 0.4, 0.2, 1]
        else:
            self.msg_label.color = list(RED)
            self.msg_label.text  = " Not enough points!"

class StudySenseApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        Thereal.load_points()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TimeSelectScreen(name="time_select"))
        sm.add_widget(SessionScreen(name="session"))
        sm.add_widget(SummaryScreen(name="summary"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(HistoryWeeklyScreen(name="weeklyview"))
        sm.add_widget(StoreScreen(name="store"))
        sm.add_widget(ItemScreen(name="item"))
        return sm

if __name__ == "__main__":
    StudySenseApp().run()
    
    

    
    
    
    
    