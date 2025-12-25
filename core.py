import logging
import time
import pyautogui
import os
import threading
import queue
import tkinter as tk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(lineno)d - %(levelname)s - %(funcName)s - %(message)s')


class Core:
    current_dir = os.getcwd()
    is_on_class_page = False
    all_class_finished = False
    stop_program = False


    def find_unstudy_class(self):

        study_button_picture = self.current_dir + '\\image\\study button.png'
        progress_bar_picture = self.current_dir + '\\image\\100 percent progress bar.png'
        turn_page_button_picture = self.current_dir + '\\image\\can change page.png'
        position_of_study_button = None
        position_of_progress_bar = None
        position_of_turn_page_button = None

        while not self.is_on_class_page:
            try:
                #检查是否在课程页面(是否找到学习按钮)
                while position_of_study_button is None:
                    logging.info("Searching for unstudied courses...")
                    time.sleep(2)
                    try:
                        position_of_study_button = pyautogui.locateAllOnScreen(study_button_picture, confidence=0.9, grayscale=True)
                    except: 
                        position_of_study_button = pyautogui.locateAllOnScreen(study_button_picture, confidence=0.9, grayscale=True)
                    time.sleep(2)

                #向下滚动页面，确保所有课程都加载出来
                pyautogui.scroll(-500)
                time.sleep(2)

                #读取学习按钮和进度条的位置
                position_of_study_button = pyautogui.locateAllOnScreen(study_button_picture, confidence=0.9, grayscale=True)
                position_of_progress_bar = pyautogui.locateAllOnScreen(progress_bar_picture, confidence=0.9, grayscale=True)

                #寻找未完成的课程并进入课程
                self.is_on_class_page = self.find_and_click_unstudy_class(position_of_study_button, position_of_progress_bar)

                #仍在选择课程页面，则判定是否可翻页
                if not self.is_on_class_page:
                    logging.info("No unstudied courses found on this page.Trying to turn the page...")
                    pyautogui.scroll(-500)
                    time.sleep(1)
                    try:
                        position_of_turn_page_button = pyautogui.locateOnScreen(turn_page_button_picture, confidence=0.9, grayscale=True)
                        pyautogui.click(position_of_turn_page_button.left + 10, position_of_turn_page_button.top + 10, duration=0.5)
                        logging.info("Turned to the next page.")
                    except:
                        logging.info("No turn page button found. Reached the end of course list. All courses may have been completed.")
                        position_of_turn_page_button = None
                        self.all_class_finished = True
                        return
                     
                else:
                    logging.info("Entering unstudied course page...")
                    self.on_class_page()
                    
            except Exception as e:
                logging.error(f"Error occurred while finding unstudied class: {e}")
                self.stop_program = True
                return

    def find_and_click_unstudy_class(self, position_of_study_button, position_of_progress_bar):

        try:
            #遍历所有学习按钮和进度条
            for position1 in position_of_study_button:
                    logging.info(f"Found study button at {position1}")
                    continue_outer = False
                    for position2 in position_of_progress_bar:
                        logging.info(f"Found progress bar at {position2}")

                    #如果进度条和按钮位置相同说明课程已完成，跳过
                        if abs(position2.top - position1.top) < position1.height:
                            logging.info("Course already completed, skipping.")
                            continue_outer = True
                            break
                    
                    if continue_outer:
                        continue

                    #否则点击学习按钮
                    logging.info("Unstudied course found.")
                    pyautogui.click(position1.left + 10, position1.top + 10, duration=0.5)#使用duration模拟人类反应速度
                    logging.info("Clicked on study button.")
                    return True
            
            logging.info("No unstudied courses found on this page.")
            return False
        
        except Exception as e:
            logging.error(f"Error occurred while finding and clicking unstudied class: {e}")  
            self.stop_program = True
            return False
    
    def on_class_page(self):  #进入指定课堂页面后

        on_class_page_picture = self.current_dir + '\\image\\is on class page.png'
        is_class_finished_picture = self.current_dir + '\\image\\finish playing button.png'
        is_class_finished = False

        try:
            #检查是否在课程页面(是否找到爱心)
            pyautogui.scroll(500)
            pyautogui.locateOnScreen(on_class_page_picture, confidence=0.6, grayscale=True)
            self.is_on_class_page = True
            logging.info("On class page.")

        except:
            #如果不在课程页面则退出函数
            self.is_on_class_page = False
            logging.warning("Not on class page but on_class_page has been trigger.")
            self.stop_program = True
            return
        
        #每隔20分钟检测课程是否播放完毕
        while is_class_finished is False:
            time.sleep(1200)
            try:
                pyautogui.locateOnScreen(is_class_finished_picture, confidence=0.5, grayscale=True)
                is_class_finished = True
                logging.info("Class finished playing.")
                self.is_on_class_page = False
                self.return_to_main_page()

            except:
                is_class_finished = False
                logging.info("Class still playing...")
                continue

    def return_to_main_page(self):
        #返回主页面

        tab_bar_picture = self.current_dir + '\\image\\tab bar.png'
        main_page_tab_picture = self.current_dir + '\\image\\main page tab.png'
        main_page_picture = self.current_dir + '\\image\\main page.png'

        logging.info("Returning to main page...")

        #寻找并打开标签栏
        try:
            tab_bar_position = pyautogui.locateOnScreen(tab_bar_picture, confidence=0.9, grayscale=True)
            logging.info("Found tab bar.")
            pyautogui.moveTo(tab_bar_position.left + 5, tab_bar_position.top + 5, duration=0.5)
        except:
            logging.error("Tab bar not found.")
            self.stop_program = True
            return
        time.sleep(2)

        #点击主页面标签
        try:
            main_page_tab_position = pyautogui.locateOnScreen(main_page_tab_picture, confidence=0.75, grayscale=True)
            logging.info("Found main page tab.")
            pyautogui.click(main_page_tab_position.left + 5, main_page_tab_position.top + 5, duration=0.5)
        except:
            logging.error("Main page tab not found.")
            self.stop_program = True
            return
        
        #确认位于主页面
        try:
            pyautogui.locateOnScreen(main_page_picture, confidence=0.9, grayscale=True)
            logging.info("Returned to main page successfully.")
            self.on_class_page = False
        except:
            logging.error("Failed to return to main page.")
            self.stop_program = True
            return
        
        pyautogui.moveTo(500, 500, duration=0.5)


class TkHandler(logging.Handler):
    def __init__(self, q):
        super().__init__()
        self.queue = q

    def emit(self, record):
        try:
            msg = self.format(record)
            self.queue.put(msg)
        except Exception:
            pass


class LogWindow:
    def __init__(self, width=900, height=240):
        self.q = queue.Queue()
        self.root = tk.Tk()
        self.root.title("实时日志")
        self.root.attributes("-topmost", True)
        # 计算水平居中并置顶位置（屏幕正上方）
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        x = max((screen_w - width) // 2, 0)
        y = 0
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.text = tk.Text(self.root, state='disabled', bg='black', fg='white')
        self.text.pack(fill='both', expand=True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False
        self.root.after(100, self.poll_queue)

    def poll_queue(self):
        try:
            while not self.q.empty():
                msg = self.q.get_nowait()
                self.append(msg + "\n")
        except Exception:
            pass
        if not self.closed:
            self.root.after(100, self.poll_queue)

    def append(self, msg):
        self.text.config(state='normal')
        self.text.insert('end', msg)
        self.text.see('end')
        self.text.config(state='disabled')

    def on_close(self):
        self.closed = True
        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self):
        try:
            self.root.mainloop()
        except Exception:
            pass

if __name__ == "__main__":
    # 创建日志窗口（但不要在子线程里 run mainloop）
    log_win = LogWindow(width=300, height=300)
    tk_handler = TkHandler(log_win.q)
    tk_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(tk_handler)

    # 启动主程序到后台线程，保证 Tk 在主线程运行
    core = Core()

    def run_core():
        while not (core.all_class_finished or core.stop_program):
            core.find_unstudy_class()
        #time.sleep(5)
        #core.return_to_main_page()    
        # 主程序结束后安全关闭日志窗口（通过 Tk 的事件循环）
        try:
            log_win.root.after(0, log_win.on_close)
        except Exception:
            pass

    threading.Thread(target=run_core, daemon=True).start()

    # 在主线程运行 Tk 主循环，确保窗口可见
    log_win.run()
