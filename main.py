import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def stitch_images(folder_path, output_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    if not files:
        return False, "文件夹中没有找到PNG文件"
    
    files.sort()
    
    images = []
    total_width = 0
    max_height = 0
    for f in files:
        img_path = os.path.join(folder_path, f)
        try:
            img = Image.open(img_path)
            images.append(img)
            total_width += img.width
            max_height = max(max_height, img.height)
        except Exception as e:
            return False, f"无法打开图像 {f}: {e}"
    
    mode = images[0].mode if images else 'RGB'
    new_img = Image.new(mode, (total_width, max_height))
    
    x_offset = 0
    for img in images:
        y_offset = (max_height - img.height) // 2
        new_img.paste(img, (x_offset, y_offset))
        x_offset += img.width
    
    try:
        new_img.save(output_path, format='PNG')
        for img in images:
            img.close()
        new_img.close()
        return True, "拼接完成"
    except Exception as e:
        return False, f"保存失败: {e}"

class RainbowStitchApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("彩虹图拼接工具by@CzXieDdan")
        self.root.geometry("500x200")
        self.root.resizable(False, False)
        
        self.folder_path = tk.StringVar()
        
        tk.Label(self.root, text="彩虹图拼接工具", font=("微软雅黑", 14, "bold")).pack(pady=15)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        tk.Label(frame, text="文件夹：").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.folder_path, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="选择文件夹", command=self.select_folder).pack(side=tk.LEFT)
        
        tk.Button(self.root, text="开始拼接并保存", font=("微软雅黑", 12), 
                  bg="#4CAF50", fg="white", command=self.start_stitch).pack(pady=20)
        
    def select_folder(self):
        path = filedialog.askdirectory(title="请选择包含PNG图片的文件夹")
        if path:
            self.folder_path.set(path)
    
    def start_stitch(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("错误", "请先选择有效的文件夹")
            return
        
        save_path = filedialog.asksaveasfilename(
            title="保存彩虹图",
            defaultextension=".png",
            filetypes=[("PNG图像", "*.png")]
        )
        if not save_path:
            return
        
        success, msg = stitch_images(folder, save_path)
        if success:
            messagebox.showinfo("成功", f"{msg}\n已保存至：{save_path}")
        else:
            messagebox.showerror("失败", msg)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RainbowStitchApp()
    app.run()
