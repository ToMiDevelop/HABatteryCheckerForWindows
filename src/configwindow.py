# basic imports

from pathlib import Path
import customtkinter as ctk
from dotenv import set_key

# Custom imports

from messages import configWindow

# Dark theme enabling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ConfigWindow(ctk.CTk):

    def __init__(self, env_path: Path):
        super().__init__()
        self.env_path = env_path

        self.title(f"{configWindow["plTitle"]}")
        self.geometry("520x620")
        self.resizable(False, False)

        # Main header
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

        # --- Sekcja Home Assistant ---
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

        # --- Sekcja Gemini API ---
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
        self.gemini_key_entry.pack(padx=15, pady=(5, 15))

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
        self.save_button.pack(fill="x", padx=20, pady=(10, 20))

    def save_config(self):
        ha_url = self.ha_url_entry.get().strip()
        ha_token = self.ha_token_entry.get().strip()
        gemini_key = self.gemini_key_entry.get().strip()

        # Simple validation
        if not ha_url or not ha_token or not gemini_key:
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

        print(f"{configWindow["plConfigSavedMessage"]}")
        self.destroy()  # Zamkcie okna po udanym zapisie


def showConfigWindow(env_path: Path):
    app = ConfigWindow(env_path)
    app.mainloop()


if __name__ == "__main__":
    # local test
    env_file = Path(__file__).resolve().parent / ".env"
    show_config_window(env_file)