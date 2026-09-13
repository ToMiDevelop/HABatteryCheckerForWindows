# basic imports

from pathlib import Path
import customtkinter as ctk
from dotenv import set_key
import webbrowser
from PIL import Image, ImageDraw,ImageOps
import sys

# Custom imports

from messages import configWindow

# Dark theme enabling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ConfigWindow(ctk.CTk):

    @staticmethod
    def resourcePath(relative_path: str) -> Path:
        """Returns the path to a resource embedded in the .exe (PyInstaller --onefile)
        or to the source file in development mode."""
        if hasattr(sys, "_MEIPASS"):
            # noinspection PyProtectedMember
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).resolve().parent
        return base_path / relative_path

    def __init__(self, env_path: Path):
        super().__init__()

        # obtaining base dir and setting author.png path
        self.AUTH_DIR = self.resourcePath("pics/author.png")

        # env path variable
        self.env_path = env_path

        # windows title
        self.title(f"{configWindow["plTitle"]}")

        # window geometry
        self.geometry("650x690")
        self.resizable(False, False)

        # --- Main Header Section ---
        self.header_label = ctk.CTkLabel(
            self,
            text=f"⚙️ {configWindow["plMainHeaderText"]}",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.header_label.pack(padx=20, pady=(20, 10))

        self.sub_label = ctk.CTkLabel(
            self,
            text=f"{configWindow["plMainHeaderSubLabelText"]}",
            wraplength=450,
            text_color="gray",
        )
        self.sub_label.pack(padx=20, pady=(0, 20))

        # --- Home Assistant Section ---
        self.ha_frame = ctk.CTkFrame(self)
        self.ha_frame.pack(fill="x", padx=20, pady=10)

        self.ha_title = ctk.CTkLabel(
            self.ha_frame,
            text="Home Assistant",
            font=ctk.CTkFont(weight="bold"),
        )
        self.ha_title.pack(anchor="w", padx=15, pady=(10, 5))

        self.ha_url_entry = ctk.CTkEntry(
            self.ha_frame,
            placeholder_text=f"{configWindow["plMAinHeaderHAIpText"]}",
            width=450,
        )
        self.ha_url_entry.pack(padx=15, pady=5)

        self.ha_token_entry = ctk.CTkEntry(
            self.ha_frame,
            placeholder_text=f"{configWindow["plMainHeaderHALongLiveTokenText"]}",
            show="*",
            width=450,
        )
        self.ha_token_entry.pack(padx=15, pady=(5, 15))

        # --- Gemini API Section---
        self.gemini_frame = ctk.CTkFrame(self)
        self.gemini_frame.pack(fill="x", padx=20, pady=10)

        self.gemini_title = ctk.CTkLabel(
            self.gemini_frame, text="Gemini API", font=ctk.CTkFont(weight="bold")
        )
        self.gemini_title.pack(anchor="w", padx=15, pady=(10, 5))

        self.gemini_key_entry = ctk.CTkEntry(
            self.gemini_frame,
            placeholder_text=f"{configWindow["plMainHeaderAPIGeminiText"]}",
            show="*",
            width=450,
        )
        self.gemini_key_entry.pack(padx=15, pady=5)

        self.gemini_model_entry = ctk.CTkEntry(
            self.gemini_frame,
            placeholder_text=f"{configWindow["plMainHeaderGeminiModelText"]}",
            width=450,
        )
        self.gemini_model_entry.pack(padx=15, pady=(5, 15))

        # Status Error / Info
        self.status_label = ctk.CTkLabel(
            self, text="", text_color="red", font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)

        # Save button
        self.save_button = ctk.CTkButton(
            self,
            text=f"{configWindow["plSaveButtonText"]}",
            command=self.save_config,
            height=40,
            font=ctk.CTkFont(weight="bold"),
        )
        self.save_button.pack(fill="x", padx=20, pady=(10, 35))

        # --- Author Footer Section---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.avatar_image = self.get_circular_avatar(self.AUTH_DIR, size=(75, 75))
        self.avatar_label = ctk.CTkLabel(
            self.footer_frame,
            image=self.avatar_image,
            text=""
        )
        self.author_text_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"{configWindow['plCreatedBy']} 🚀",
            font=ctk.CTkFont(size=16, underline=False),
            text_color=("#1f538d", "#1f6aa5"),  # color reacting to light / dark theme
            cursor="hand2"
        )
        self.create_author_footer()

        # --- Disclaimer bottom text ---
        self.disclaimer_label = ctk.CTkLabel(
            self,
            text=f"{configWindow['plDisclaimer']}",
            font=ctk.CTkFont(size=15, underline=False),
            wraplength=620,
            text_color="gray",
            justify="left",
            anchor="center"
        )
        self.disclaimer_label.pack(fill='x', padx=20, pady=(15, 20))

    @staticmethod
    def open_author_site(event=None):
        webbrowser.open_new_tab("https://tomidevelop.github.io")

    @staticmethod
    def get_circular_avatar(imagePath: Path, size: tuple = (70, 70)):
        """Loads image, adjusts it and cuts to a circle."""
        if not imagePath.exists():
            return None
        img = Image.open(imagePath).convert("RGBA")
        # Crop to rectangle with set size
        img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
        # Creating circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        img.putalpha(mask)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    def create_author_footer(self):
        # Author container
        self.footer_frame.pack(pady=(0, 10))
        self.footer_frame.bind("<Button-1>", self.open_author_site)

        # Attempt to load the avatar
        if self.avatar_image:
            self.avatar_label.pack(side="left", padx=(0, 25), pady=(0,0))
            self.avatar_label.bind("<Button-1>", self.open_author_site)

        # Text with link
        self.author_text_label.pack(side="left")
        self.author_text_label.bind("<Button-1>", self.open_author_site)


    def on_close(self):
        print("Closing app, config windows closed without usage...")
        self.destroy()

    def save_config(self):
        ha_url = self.ha_url_entry.get().strip()
        ha_token = self.ha_token_entry.get().strip()
        gemini_key = self.gemini_key_entry.get().strip()
        gemini_model = self.gemini_model_entry.get().strip()

        # Simple validation
        if not ha_url or not ha_token or not gemini_key or not gemini_model:
            self.status_label.configure(
                text=f"❌ {configWindow["plSimpleValidationText"]}", text_color="red"
            )
            return

        # .env file creation if does not exist
        if not self.env_path.exists():
            self.env_path.touch()

        # Save to .env file
        set_key(str(self.env_path), "HA_URL", ha_url)
        set_key(str(self.env_path), "HA_TOKEN", ha_token)
        set_key(str(self.env_path), "GEMINI_API_KEY", gemini_key)
        set_key(str(self.env_path), "GEMINI_MODEL_NAME", gemini_model)

        print(f"{configWindow["plConfigSavedMessage"]}")
        self.destroy()  # Zamkcie okna po udanym zapisie


def showConfigWindow(env_path: Path):
    app = ConfigWindow(env_path)
    app.mainloop()


# if __name__ == "__main__":
#     # local test
#     env_file = Path(__file__).resolve().parent / ".env"
#     show_config_window(env_file)