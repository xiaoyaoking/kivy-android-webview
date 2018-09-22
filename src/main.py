from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.logger import Logger

from kivy.clock import Clock    
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty     
from kivy.core.window import Window
                              
from jnius import autoclass                                                                     
from android.runnable import run_on_ui_thread
from xyweb.webviewengine import WebviewEngine

Builder.load_string("""
<ShapeBuilder>:
    TextInput: 
        id: address_bar
        size_hint_y: None
        height: '32dp'
        multiline: False
        hint_text: 'SNMP Community String(s)'
        text: 'http://www.526net.com'
        pos_hint: {"top": 1, 'left': 1}
    BoxLayout:
        id: content_window
        size_hint_y: None
        height: "48dp"
        spacing: "2dp"
        padding: "2dp"

    BoxLayout:
        id: browser_toolbar
        size_hint_y: None
        height: "48dp"
        spacing: "2dp"
        padding: "2dp"

        ToggleButton:
            text: "Debug"
            id: debug
            on_release: root.build()
        Button:
            text: "New shape"
            on_release: root.push_shape()
        Button:
            text: "Build"
            on_release: root.build()
        Button:
            text: "Reset"
            on_release: root.reset()
""")


class ShapeBuilder(FloatLayout):
	webviewEngine = None
	#address box 
	address_bar = ObjectProperty(None)
	#can Go Back
	can_go_back = BooleanProperty(False)
	#can go forward 
	can_go_forward = BooleanProperty(False)

	def __init__(self, **kwargs):
		super(ShapeBuilder, self).__init__(**kwargs)
		Clock.schedule_once(self._on_init_complete,0)
		#self._on_init_complete()

	@run_on_ui_thread
	def _on_init_complete(self,*args):
		#address bar 
		bottom_toolbar_height = 100
		#Logger.info('ids: {}'.format(self.ids))
		self.address_bar = self.ids.address_bar

		#self.top_right_nav = self.ids.top_right_nav 

		#lets check if webview object has been instantiated already
		if(self.webviewEngine is not None):
			return True 
		
		webview_pos_y = self.ids.browser_toolbar.height

		contentWin = self.ids.content_window
		
		contentWinHeight = Window.height - (webview_pos_y + bottom_toolbar_height)
		 
		print('----!!___WInDOW WIDTH-------',Window.width) 

		#init webview engine 
		self.webviewEngine = WebviewEngine(
								posX=0,
								posY=webview_pos_y,
								width=Window.width,
								height=contentWinHeight
								)
		
		#Add webview engine class as a widget
		contentWin.add_widget(self.webviewEngine)

		#Listen to events 
		self.webviewEngine.bind(on_page_started=self.proccess_on_page_start)
		
		#On on_page_commit_visible
		self.webviewEngine.bind(on_page_commit_visible=self.proccess_on_page_commit_visible)

		self.webviewEngine.bind(on_should_override_url_loading=self.on_should_override_url_loading)
		


	#proccess back button 
	def proccess_go_back(self):
		
		#if page can go back, then go back 
		if(self.can_go_back == True):
			self.webviewEngine.goBack()

	#Proccess Go Back 
	def proccess_go_forward(self):

		#if can go forward, then go 
		if(self.can_go_forward == True):
			self.webviewEngine.goForward()
	

	#enable disable back and forward button
	def proccess_on_page_start(self,*args,**kwargs):
		
		#change the url to the new url 
		new_url = kwargs.get('url')

		if(new_url is not None):
			self.update_address_bar_url(new_url)


	#proccess on Page Commit visible 
	def proccess_on_page_commit_visible(self,*args,**kwargs):

		#if the webview can go back, update the button
		self.can_go_back = self.webviewEngine.canGoBack()

		#check if it can go forward 
		self.can_go_forward = self.webviewEngine.canGoForward()



	#should_override_url_loading
	def on_should_override_url_loading(self,*args,**kwargs):

		#change the url to the new url 
		new_url = kwargs.get('url')

class TessApp(App):
    def build(self):
        return ShapeBuilder()


TessApp().run()
