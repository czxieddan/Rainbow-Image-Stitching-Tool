import os
import struct
import webbrowser
from tkinter import Tk, Label, Button, Frame, StringVar, filedialog, messagebox, ttk
from PIL import Image

translations = {
    'en': {
        'app_title': 'Rainbow Image Stitching Tool by @CzXieDdan',
        'main_label': 'Rainbow Image Stitching Tool',
        'input_label': 'Input Source:',
        'select_folder': 'Select Folder',
        'select_files': 'Select Files',
        'no_selection': 'No input selected',
        'folder_selected': 'Folder: {}',
        'files_selected': '{} files selected',
        'export_format': 'Export Format:',
        'png': 'PNG (lossless)',
        'dds_uncomp': 'DDS (B8G8R8A8)',
        'dds_bc3': 'DDS (BC3/DXT5)',
        'start_button': 'Stitch and Save',
        'github_button': 'Project GitHub',
        'language_label': 'Language:',
        'save_dialog_title': 'Save Stitched Image',
        'png_filetype_desc': 'PNG Files',
        'dds_filetype_desc': 'DDS Files',
        'open_files_desc': 'Image Files',
        'success_title': 'Success',
        'success': 'Stitching completed',
        'saved_to': 'Saved to: {}',
        'error_no_input': 'Please select an input source first',
        'error_no_images': 'No supported image files found',
        'error_open': 'Cannot open image {}: {}',
        'error_save': 'Save failed: {}',
        'error_dds_unsupported': 'Only uncompressed B8G8R8A8 DDS supported for manual loading',
        'invalid_dds_magic': 'Invalid DDS file identifier',
        'error_bc3_size': 'BC3 compression requires final image width and height to be multiples of 4',
        'error': 'Error',
    },
    'zh_cn': {
        'app_title': '彩虹图像拼接工具 by @CzXieDdan',
        'main_label': '彩虹图像拼接工具',
        'input_label': '输入来源：',
        'select_folder': '选择文件夹',
        'select_files': '选择多个文件',
        'no_selection': '未选择输入来源',
        'folder_selected': '文件夹：{}',
        'files_selected': '已选中 {} 个文件',
        'export_format': '导出格式：',
        'png': 'PNG（无损）',
        'dds_uncomp': 'DDS（B8G8R8A8）',
        'dds_bc3': 'DDS（BC3/DXT5）',
        'start_button': '开始拼接并保存',
        'github_button': '项目 GitHub 地址',
        'language_label': '语言：',
        'save_dialog_title': '保存拼接图像',
        'png_filetype_desc': 'PNG 文件',
        'dds_filetype_desc': 'DDS 文件',
        'open_files_desc': '图像文件',
        'success_title': '成功',
        'success': '拼接完成',
        'saved_to': '已保存至：{}',
        'error_no_input': '请先选择输入来源',
        'error_no_images': '未找到支持的图像文件',
        'error_open': '无法打开图像 {}: {}',
        'error_save': '保存失败：{}',
        'error_dds_unsupported': '手动加载仅支持无压缩 B8G8R8A8 DDS',
        'invalid_dds_magic': '无效的DDS文件标识',
        'error_bc3_size': 'BC3压缩要求最终拼接图像宽度和高度为4的倍数',
        'error': '错误',
    },
    'zh': {
        'app_title': '彩虹圖像拼接工具 by @CzXieDdan',
        'main_label': '彩虹圖像拼接工具',
        'input_label': '輸入來源：',
        'select_folder': '選擇資料夾',
        'select_files': '選擇多個檔案',
        'no_selection': '未選擇輸入來源',
        'folder_selected': '資料夾：{}',
        'files_selected': '已選取 {} 個檔案',
        'export_format': '匯出格式：',
        'png': 'PNG（無損）',
        'dds_uncomp': 'DDS（B8G8R8A8）',
        'dds_bc3': 'DDS（BC3/DXT5）',
        'start_button': '開始拼接並儲存',
        'github_button': '專案 GitHub 位址',
        'language_label': '語言：',
        'save_dialog_title': '儲存拼接圖像',
        'png_filetype_desc': 'PNG 檔案',
        'dds_filetype_desc': 'DDS 檔案',
        'open_files_desc': '圖像檔案',
        'success_title': '成功',
        'success': '拼接完成',
        'saved_to': '已儲存至：{}',
        'error_no_input': '請先選擇輸入來源',
        'error_no_images': '未找到支援的圖像檔案',
        'error_open': '無法開啟圖像 {}: {}',
        'error_save': '儲存失敗：{}',
        'error_dds_unsupported': '手動載入僅支援無壓縮 B8G8R8A8 DDS',
        'invalid_dds_magic': '無效的DDS檔案標識',
        'error_bc3_size': 'BC3壓縮要求最終拼接圖像寬度和高度為4的倍數',
        'error': '錯誤',
    },
    'ha': {
        'app_title': 'Ha Ha Ha Ha by @CzXieDdan',
        'main_label': 'Ha Ha Ha Ha',
        'input_label': 'Ha Ha：',
        'select_folder': 'Ha Ha Ha',
        'select_files': 'Ha Ha Ha ',
        'no_selection': 'Ha Ha Ha Ha',
        'folder_selected': 'Ha：{}',
        'files_selected': 'Ha Ha {} Ha Ha',
        'export_format': 'Ha Ha：',
        'png': 'Ha（Ha）',
        'dds_uncomp': 'Ha（HaHaHaHa）',
        'dds_bc3': 'Ha（Ha/Ha）',
        'start_button': 'Ha Ha Ha Ha',
        'github_button': 'Ha GitHub Ha',
        'language_label': 'Ha：',
        'save_dialog_title': 'Ha Ha Ha',
        'png_filetype_desc': 'Ha Ha',
        'dds_filetype_desc': 'Ha Ha',
        'open_files_desc': 'Ha Ha',
        'success_title': 'Ha Ha Ha',
        'success': 'Ha Ha Ha',
        'saved_to': 'Ha Ha：{}',
        'error_no_input': 'Ha Ha Ha Ha',
        'error_no_images': 'Ha Ha Ha Ha Ha',
        'error_open': 'Ha {}: {}',
        'error_save': 'Ha：{}',
        'error_dds_unsupported': 'Ha Ha Ha Ha',
        'invalid_dds_magic': 'Ha',
        'error_bc3_size': 'Ha',
        'error': 'Ha',
    }
}

class RainbowStitchApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("彩虹图像拼接工具 by @CzXieDdan")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.current_lang = 'en'
        self.lang_map = {'English': 'en', '简体中文': 'zh_cn', '繁体中文': 'zh', 'Ha': 'ha'}

        self.input_mode = None
        self.input_data = None

        self.build_ui()
        self.update_language()

    def t(self, key, *args):
        text = translations[self.current_lang].get(key, key)
        return text.format(*args) if args else text

    def build_ui(self):
        self.main_label = Label(self.root, text="", font=("微软雅黑", 16, "bold"))
        self.main_label.pack(pady=20)

        input_frame = Frame(self.root)
        input_frame.pack(pady=10)

        self.input_label = Label(input_frame, text="", font=("微软雅黑", 10))
        self.input_label.pack()

        btn_frame = Frame(input_frame)
        btn_frame.pack(pady=8)

        self.select_folder_btn = Button(btn_frame, text="", width=18, command=self.select_folder)
        self.select_folder_btn.pack(side='left', padx=10)

        self.select_files_btn = Button(btn_frame, text="", width=18, command=self.select_files)
        self.select_files_btn.pack(side='left', padx=10)

        self.detail_label = Label(input_frame, text="", fg="gray")
        self.detail_label.pack(pady=5)

        export_frame = Frame(self.root)
        export_frame.pack(pady=15)

        self.export_label = Label(export_frame, text="", font=("微软雅黑", 10))
        self.export_label.grid(row=0, column=0, columnspan=3)

        self.export_var = StringVar(value='png')

        self.png_radio = ttk.Radiobutton(export_frame, text="", variable=self.export_var, value='png')
        self.png_radio.grid(row=1, column=0, padx=20)

        self.dds_uncomp_radio = ttk.Radiobutton(export_frame, text="", variable=self.export_var, value='dds_uncomp')
        self.dds_uncomp_radio.grid(row=1, column=1, padx=20)

        self.dds_bc3_radio = ttk.Radiobutton(export_frame, text="", variable=self.export_var, value='dds_bc3')
        self.dds_bc3_radio.grid(row=1, column=2, padx=20)

        self.start_btn = Button(self.root, text="", font=("微软雅黑", 12), bg="#4CAF50", fg="white",
                                width=20, height=2, command=self.start_stitch)
        self.start_btn.pack(pady=20)

        bottom_frame = Frame(self.root, bg="#f0f0f0", height=60)
        bottom_frame.pack(side='bottom', fill='x', pady=(0, 20))

        lang_frame = Frame(bottom_frame, bg="#f0f0f0")
        lang_frame.pack(side='left', padx=40)

        self.lang_label = Label(lang_frame, text="", bg="#f0f0f0", font=("微软雅黑", 10))
        self.lang_label.pack(side='left')

        self.lang_combo = ttk.Combobox(lang_frame, values=list(self.lang_map.keys()), state='readonly', width=12)
        self.lang_combo.pack(side='left', padx=8)
        self.lang_combo.bind('<<ComboboxSelected>>', self.change_language)

        self.github_btn = Button(bottom_frame, text="", bg="#0366d6", fg="white", font=("微软雅黑", 10, "bold"),
                                 command=self.open_github, relief='flat', padx=10, pady=5)
        self.github_btn.pack(side='right', padx=40)

    def update_language(self):
        self.root.title(self.t('app_title'))
        self.main_label.config(text=self.t('main_label'))
        self.input_label.config(text=self.t('input_label'))
        self.select_folder_btn.config(text=self.t('select_folder'))
        self.select_files_btn.config(text=self.t('select_files'))
        self.detail_label.config(text=self.t('no_selection'))
        self.export_label.config(text=self.t('export_format'))
        self.png_radio.config(text=self.t('png'))
        self.dds_uncomp_radio.config(text=self.t('dds_uncomp'))
        self.dds_bc3_radio.config(text=self.t('dds_bc3'))
        self.start_btn.config(text=self.t('start_button'))
        self.lang_label.config(text=self.t('language_label'))
        self.github_btn.config(text=self.t('github_button'))

        display_name = [k for k, v in self.lang_map.items() if v == self.current_lang][0]
        self.lang_combo.set(display_name)

        self.set_input_detail()

    def change_language(self, event=None):
        selection = self.lang_combo.get()
        self.current_lang = self.lang_map.get(selection, 'zh_cn')
        self.update_language()

    def set_input_detail(self):
        if self.input_mode == 'folder':
            text = self.t('folder_selected', self.input_data)
        elif self.input_mode == 'files':
            text = self.t('files_selected', len(self.input_data))
        else:
            text = self.t('no_selection')
        self.detail_label.config(text=text)

    def select_folder(self):
        path = filedialog.askdirectory(title=self.t('select_folder'))
        if path:
            self.input_mode = 'folder'
            self.input_data = path
            self.set_input_detail()

    def select_files(self):
        files = filedialog.askopenfilenames(
            title=self.t('select_files'),
            filetypes=[(self.t('open_files_desc'), "*.png *.dds")]
        )
        if files:
            self.input_mode = 'files'
            self.input_data = list(files)
            self.set_input_detail()

    def open_github(self):
        webbrowser.open("https://github.com/czxieddan/Rainbow-Image-Stitching-Tool")

    def load_image(self, path):
        try:
            return Image.open(path).convert('RGBA')
        except Exception as e:
            if path.lower().endswith('.dds'):
                return self.load_dds_uncomp(path)
            raise ValueError(self.t('error_open', os.path.basename(path), str(e)))

    def load_dds_uncomp(self, path):
        with open(path, 'rb') as f:
            if f.read(4) != b'DDS ':
                raise ValueError(self.t('invalid_dds_magic'))
            f.seek(12)
            height = struct.unpack('<I', f.read(4))[0]
            width = struct.unpack('<I', f.read(4))[0]
            f.seek(84)
            fourcc = f.read(4)
            if fourcc != b'DX10':
                raise ValueError(self.t('error_dds_unsupported'))
            f.seek(128)
            dxgi_format = struct.unpack('<I', f.read(4))[0]
            if dxgi_format != 87:
                raise ValueError(self.t('error_dds_unsupported'))
            f.seek(148)
            data = f.read(width * height * 4)
            img = Image.frombytes('BGRA', (width, height), data)
            return img.convert('RGBA')

    def save_dds_uncomp(self, image, path):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        bgra = image.convert('BGRA')
        data = bgra.tobytes()
        width, height = image.size

        header = bytearray(148)
        header[0:4] = b'DDS '
        struct.pack_into('<I', header, 4, 124)
        struct.pack_into('<I', header, 8, 0x0000100F)
        struct.pack_into('<I', header, 12, height)
        struct.pack_into('<I', header, 16, width)
        struct.pack_into('<I', header, 20, width * 4)
        struct.pack_into('<I', header, 28, 0)
        struct.pack_into('<I', header, 76, 32)
        struct.pack_into('<I', header, 80, 0x4)
        header[84:88] = b'DX10'
        struct.pack_into('<I', header, 108, 0x1000)
        struct.pack_into('<I', header, 128, 87)
        struct.pack_into('<I', header, 132, 3)
        struct.pack_into('<I', header, 140, 1)

        with open(path, 'wb') as f:
            f.write(header)
            f.write(data)

    def start_stitch(self):
        if not self.input_mode:
            messagebox.showerror(self.t('error'), self.t('error_no_input'))
            return

        if self.input_mode == 'folder':
            files = [f for f in os.listdir(self.input_data) if f.lower().endswith(('.png', '.dds'))]
            files.sort(key=str.lower)
            img_paths = [os.path.join(self.input_data, f) for f in files]
        else:
            img_paths = sorted(self.input_data, key=lambda p: os.path.basename(p).lower())

        if not img_paths:
            messagebox.showerror(self.t('error'), self.t('error_no_images'))
            return

        images = []
        total_width = 0
        max_height = 0
        for path in img_paths:
            try:
                img = self.load_image(path)
                images.append(img)
                total_width += img.width
                max_height = max(max_height, img.height)
            except Exception as e:
                messagebox.showerror(self.t('error'), str(e))
                for im in images: im.close()
                return

        new_img = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))

        x_offset = 0
        for img in images:
            y_offset = (max_height - img.height) // 2
            new_img.paste(img, (x_offset, y_offset))
            x_offset += img.width

        export_type = self.export_var.get()

        if export_type == 'dds_bc3':
            if total_width % 4 != 0 or max_height % 4 != 0:
                messagebox.showerror(self.t('error'), self.t('error_bc3_size'))
                for img in images: img.close()
                new_img.close()
                return

        dialog_title = self.t('save_dialog_title')
        if export_type == 'png':
            filetypes = [(self.t('png_filetype_desc'), "*.png")]
            def_ext = ".png"
        else:
            filetypes = [(self.t('dds_filetype_desc'), "*.dds")]
            def_ext = ".dds"

        save_path = filedialog.asksaveasfilename(
            title=dialog_title,
            defaultextension=def_ext,
            filetypes=filetypes
        )
        if not save_path:
            for img in images: img.close()
            new_img.close()
            return

        try:
            if export_type == 'png':
                new_img.save(save_path, format='PNG')
            elif export_type == 'dds_uncomp':
                self.save_dds_uncomp(new_img, save_path)
            elif export_type == 'dds_bc3':
                new_img.save(save_path, format="DDS", pixel_format="DXT5")
        except Exception as e:
            messagebox.showerror(self.t('error'), self.t('error_save', str(e)))
            for img in images: img.close()
            new_img.close()
            return

        messagebox.showinfo(self.t('success_title'), f"{self.t('success')}\n{self.t('saved_to', save_path)}")

        for img in images:
            img.close()
        new_img.close()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = RainbowStitchApp()
    app.run()
