import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QPushButton, 
                             QListWidget, QLabel, QInputDialog, QMessageBox)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

# Tentukan direktori tempat file catatan akan disimpan
NOTES_DIR = "my_notes" 

class NoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Catatan Sederhana")
        self.setGeometry(100, 100, 800, 600)
        
        # Buat direktori jika belum ada
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)
            
        self.init_ui()
        self.load_file_list() # Muat daftar file saat aplikasi dimulai

    def init_ui(self):
        # 1. Tata Letak Utama (Vertical)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # 2. Area Teks Catatan
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Tulis catatan Anda di sini...")
        main_layout.addWidget(self.text_edit, 2) # Mengambil 2/3 ruang vertikal

        # 3. Bagian Bawah (Daftar File dan Kontrol)
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        # 3a. Daftar File Catatan
        file_list_frame = QVBoxLayout()
        list_label = QLabel("Daftar File Catatan:")
        list_label.setStyleSheet("font-weight: bold;")
        file_list_frame.addWidget(list_label)
        
        self.list_widget = QListWidget()
        # Hubungkan klik item pada list dengan fungsi pemuatan
        self.list_widget.itemClicked.connect(self.load_note) 
        file_list_frame.addWidget(self.list_widget)
        bottom_layout.addLayout(file_list_frame, 1) # Mengambil 1/3 ruang horizontal

        # 3b. Kontrol (Tombol)
        control_layout = QVBoxLayout()
        
        save_button = QPushButton("💾 Simpan Catatan Baru")
        save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        save_button.clicked.connect(self.save_note)
        control_layout.addWidget(save_button)
        
        # Tombol untuk memperbarui catatan yang sedang dimuat
        update_button = QPushButton("✏️ Perbarui Catatan Terpilih")
        update_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        update_button.clicked.connect(self.update_note)
        control_layout.addWidget(update_button)

        # Tombol hapus
        delete_button = QPushButton("🗑️ Hapus Catatan Terpilih")
        delete_button.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
        delete_button.clicked.connect(self.delete_note)
        control_layout.addWidget(delete_button)
        
        control_layout.addStretch(1) # Dorong tombol ke atas
        
        bottom_layout.addLayout(control_layout, 1) # Mengambil 1/3 ruang horizontal
        
        main_layout.addLayout(bottom_layout, 1) # Mengambil 1/3 ruang vertikal
        self.setLayout(main_layout)
        
        # Pengaturan Warna Latar Belakang Jendela
        self.set_background_color(QColor('#F0F0F0')) # Abu-abu muda

    def set_background_color(self, color):
        """Mengatur warna latar belakang jendela utama."""
        palette = self.palette()
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)
        
    def load_file_list(self):
        """Memuat dan menampilkan semua file .txt di direktori NOTES_DIR."""
        self.list_widget.clear()
        try:
            # Filter hanya file .txt
            files = [f for f in os.listdir(NOTES_DIR) if f.endswith('.txt')]
            self.list_widget.addItems(files)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat daftar file: {e}")

    def save_note(self):
        """Menyimpan konten QTextEdit ke file baru."""
        text_content = self.text_edit.toPlainText()
        if not text_content.strip():
            QMessageBox.warning(self, "Peringatan", "Catatan tidak boleh kosong!")
            return

        # Minta nama file dari pengguna
        file_name, ok = QInputDialog.getText(self, 'Simpan Catatan', 
                                              'Masukkan nama file untuk catatan (tanpa .txt):')

        if ok and file_name:
            final_file_name = f"{file_name.strip()}.txt"
            file_path = os.path.join(NOTES_DIR, final_file_name)
            
            # Cek jika file sudah ada
            if os.path.exists(file_path):
                reply = QMessageBox.question(self, 'Konfirmasi',
                    "File sudah ada. Timpa (overwrite)?", 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                QMessageBox.information(self, "Sukses", f"Catatan berhasil disimpan sebagai **{final_file_name}**.")
                self.text_edit.clear()
                self.load_file_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan file: {e}")
    
    def load_note(self, item):
        """Memuat catatan yang dipilih dari QListWidget ke QTextEdit."""
        file_name = item.text()
        file_path = os.path.join(NOTES_DIR, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_edit.setText(content)
            self.setWindowTitle(f"Aplikasi Catatan Sederhana - {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat file: {e}")

    def update_note(self):
        """Memperbarui konten catatan yang sedang aktif (terpilih di list)."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Peringatan", "Pilih file yang ingin diperbarui terlebih dahulu.")
            return

        file_name = selected_items[0].text()
        file_path = os.path.join(NOTES_DIR, file_name)
        text_content = self.text_edit.toPlainText()

        if not text_content.strip():
            QMessageBox.warning(self, "Peringatan", "Isi catatan tidak boleh kosong untuk diperbarui!")
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            QMessageBox.information(self, "Sukses", f"Catatan **{file_name}** berhasil diperbarui.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memperbarui file: {e}")

    def delete_note(self):
        """Menghapus catatan yang dipilih."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Peringatan", "Pilih file yang ingin dihapus terlebih dahulu.")
            return

        file_name = selected_items[0].text()
        reply = QMessageBox.question(self, 'Konfirmasi Hapus',
            f"Apakah Anda yakin ingin menghapus file **{file_name}**?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            file_path = os.path.join(NOTES_DIR, file_name)
            try:
                os.remove(file_path)
                QMessageBox.information(self, "Sukses", f"File **{file_name}** berhasil dihapus.")
                self.text_edit.clear() # Kosongkan editor
                self.setWindowTitle("Aplikasi Catatan Sederhana")
                self.load_file_list() # Muat ulang daftar
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menghapus file: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())