import devices

# messages used in toasts and LLM prompts

toastsMessage = {
    "plToastTitle": "Monitor Baterii Home Assistant",
    "plEmptyBattery": "Bateria rozładowana :(",
    "plLowBattery": "Bateria bliska rozładowaniu",
    "plNormalBattery" : "Poziom baterii"
}

# Gemini prompts

geminiPrompts = {
    "plSystemPrompt": (
    "Jesteś ekspertką/ekspertem ds. diagnostyki urządzeń Zigbee w środowisku Home Assistant. "
    "Twoim zadaniem jest ocena stanu naładowania baterii oraz analiza wpływu jakości połączenia radiowego "
    "(umiejscowienia w sieci mesh) na tempo rozładowania ogniw.\n\n"
    
    "STRUKTURA DANYCH WEJŚCIOWYCH:\n"
    "- 'batteriespercent': tabela z poziomem naładowania baterii (kolumna 'value' [%]).\n"
    "- 'deviceslqi': tabela z jakością sygnału LQI (kolumna 'value', zakres 0-255).\n"
    "- 'devicesrssi': tabela z siłą sygnału RSSI (kolumna 'value' [dBm]).\n"
    "- Dane łączysz po unikalnej nazwie urządzenia z kolumny 'name'.\n"
    "- Kolumna 'date' zawiera stempel czasu pomiaru.\n"
    "- Kolumnę 'entity_id' ignorujesz.\n"
    "- Danę są wklejone w prompt formie struktury json.\n\n"
    
    "ZASADY ANALIZY I WNIOSKOWANIA:\n"
    f"1. STAN BATERII: Baterie z poziomem 'value' < {devices.batteryThreshold}% uznawaj za krytyczne (krytyczny poziom, rozładowanie w ~2 tygodnie).\n"
    "2. DRENAŻ MESH: Urządzenia ze słabym LQI/RSSI (częste retransmisje i wysoka moc nadawania) drenują baterię znacznie szybciej. "
    "Wskaż urządzenia, których położenie w sieci pogarsza żywotność ogniwa.\n\n"
    
    "FORMAT ODPOWIEDZI:\n"
    "- Odpowiedź sformatuj w czytelnym Markdownie (używaj wypunktowań, pogrubień oraz tabel).\n"
    "- Wyraźnie wyodrębnij sekcję urządzeń wymagających PILNEJ wymiany baterii.\n"
    "- Dodaj sekcję z rekomendacjami dotyczącymi poprawy zasięgu sieci Zigbee dla najbardziej obciążonych urządzeń."
    ),
    "plPromptStart": (
        "Czy któraś z baterii obecnych w analizowanych urządzeniach rozładuje się w przeciągu najbliższych 2 tygodni?\n"
        "Oto aktualne dane z bazy:\n\n"
    )
}

footers = {
    "plFooter": "Raport wygenerowany automatycznie przez Home Assistant Battery Monitor z pomocą Google Gemini AI.",
    "plTokens": "Ilość tokenów zużytych w zapytaniu:",
    "plTokensNone": "nieznane"
}

configWindow = {
    "plTitle": "Monitor Baterii Home Assistant - Pierwsze Uruchomienie",
    "plMainHeaderText": "Konfiguracja Aplikacji",
    "plMainHeaderSubLabelText": "Przed pierwszym uruchomieniem uzupełnij dane dostępowe.\nBez nich nie połączysz się z Home Assistant oraz Gemini API.",
    "plMAinHeaderHAIpText": "http://homeassistant.local:8123 lub IP",
    "plMainHeaderHALongLiveTokenText": "Długowieczny token dostępowy (Long-Lived Access Token)",
    "plMainHeaderAPIGeminiText": "Klucz API Gemini (AI Studio)",
    "plMainHeaderGeminiModelText": "Nazwa modelu LLM (zalecany gemini-3.5-flash-lite)",
    "plSaveButtonText": "Zapisz konfigurację i uruchom",
    "plSimpleValidationText": "Wypełnij wszystkie pola przed zapisem!",
    "plConfigSavedMessage": "Zapisano dane do pliku .env!",
    "plCreatedBy": "Stworzone przez ToMiDevelop",
    "plDisclaimer": "UWAGA: Pierwsze uruchomienie aplikacji może trwać długo z powodu utworzenia lokalnej bazy danych oraz pierwszorazowego jej zasilenia."
}