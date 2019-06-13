import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login(object):
    def __init__(self, username, password, browser):
        """初始化浏览器对象，url，用户名，密码"""
        self.url = 'https://passport.zhaopin.com/login?bkUrl=https://i.zhaopin.com/blank?https%3A%2F%2Fwww.zhaopin.com%2F'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.telphone = username
        self.password = password

    def open(self):
        """打开魅族官网登录页面"""
        self.browser.get(self.url)
        print("=" * 100)
        telphone = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        print("*"*100)
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        telphone.send_keys(self.telphone)
        password.send_keys(self.password)

    def get_geetest_button(self):
        """点击滑动验证码的入口按钮"""
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        button.click()

    def get_screenshot(self):
        """获取网页截图"""
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_element(self):
        """获取验证码对象"""
        img_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        print("找到极速验证码元素")
        if img_element:
            return img_element

    def get_position(self):
        """获取验证码位置"""
        img_element = self.get_touclick_element()
        time.sleep(2)
        location = img_element.location
        size = img_element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom, left, right

    def get_geetest_image(self):
        """获取验证码图片"""
        top, bottom, left, right = self.get_position()
        print("验证码位置：", top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha

    def get_slider(self):
        """获取滑块"""
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        slider.click()
        return slider

    def is_pixel_equal(self, image1, image2, x, y):
        """判断两个像素是否相同"""
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """获取缺口偏移量"""
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """根据缺口偏移量获取运动轨迹"""
        track = []  # 移动轨迹
        current = 0  # 当前位移
        mid = distance * 4 / 5  # 减速阈值
        t = 0.2  # 计算间隔
        v = 0  # 初始速度
        while current < distance:
            if current < mid:
                a = 2  # 加速度为2
            else:
                a = -3  # 减速度为-3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1/2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        """将滑块拖动到缺口处"""
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            WebDriverWait(self.browser, 5).until(EC.text_to_be_present_in_element((By.ID, 'alertMessage_loginName'), '用户名或密码错误'))
            return self.main()
        except TimeoutException:
            return self.main()

    def get_cookies(self):
        """获取登陆成功的cookies"""
        return self.browser.get_cookies()

    def main(self):
        self.open()
        self.get_geetest_button()
        img1 = self.get_geetest_image()
        slider = self.get_slider()
        img2 = self.get_geetest_image()
        distance = self.get_gap(img1, img2)
        tracks = self.get_track(distance)
        self.move_to_gap(slider, tracks)
        self.password_error()
        cookies = self.get_cookies()
        return cookies


if __name__ == "__main__":
    login = Login()
    login.main()