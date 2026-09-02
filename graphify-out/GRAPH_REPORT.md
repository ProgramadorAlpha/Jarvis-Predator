# Graph Report - C:\Users\JoseG\OneDrive\Documentos\Jarvis Predator  (2026-09-01)

## Corpus Check
- Large corpus: 134 files · ~970,331 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 786 nodes · 1516 edges · 64 communities (46 shown, 18 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 130 edges (avg confidence: 0.6)
- Token cost: 45,754 input · 10,841 output

## Community Hubs (Navigation)
- TaskQueue
- executor.py
- file_controller.py
- youtube_video.py
- send_message.py
- browser_control
- game_updater.py
- wake_listener.py
- code_helper.py
- computer_control.py
- dev_agent.py
- screen_processor.py
- file_processor.py
- MainWindow
- JarvisLive
- Luxury wellness offering
- OpenRouterClient
- main.py
- ui.py
- FileDropZone
- desktop_control
- Cortana Assistant Layer
- memory_manager.py
- LogWidget
- JarvisUI
- config_manager.py
- computer_settings
- Smart home offering
- .__init__
- _SysMetrics
- open_app.py
- Home automation systems
- FakeUI
- Build It Now Quality Process
- MetricBar
- _SleepRequested
- Modern Tropical Villa Exterior
- Build It Now BlueLiving Partner Campaign
- ._build_config
- HudCanvas
- type_text
- Modern Villa Pool Exterior
- Ocean View Infinity Pool Villa
- Luxury Spa and Hydrotherapy Room
- MARK XXXIX-OR Upstream Assistant
- Integrated Climate Control Interior
- Smart Lock Access Control
- _get_base_dir
- _get_macos_wifi_interface
- Build It Now Construção Logo
- Sunset Pool Deck Retreat
- Night Resort Pool
- Cortana visual identity
- Home Cinema Lifestyle Scene
- B2B Supplier Network
- Design Skills Recommendations
- Jarvis Runtime Changes
- Mentor Knowledge Library
- London Remote Location Scene

## God Nodes (most connected - your core abstractions)
1. `computer_control()` - 22 edges
2. `JarvisLive` - 22 edges
3. `MainWindow` - 22 edges
4. `browser_control()` - 21 edges
5. `_call_tool()` - 20 edges
6. `file_controller()` - 19 edges
7. `_BrowserThread` - 18 edges
8. `game_updater()` - 18 edges
9. `get_api_key()` - 17 edges
10. `file_processor()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `2025 Kitchen Quote` --references--> `Build It Now Quality Process`  [EXTRACTED]
  presupuestos-referencia/presupuesto-ANTIGUO-cozinha.pdf → about-builditnow.html
- `2026 Integral Renovation Quote` --references--> `Build It Now Quality Process`  [EXTRACTED]
  presupuestos-referencia/presupuesto-NUEVO-2026.pdf → about-builditnow.html
- `JarvisLive` --uses--> `TaskPriority`  [INFERRED]
  main.py → agent/task_queue.py
- `_SleepRequested` --uses--> `TaskPriority`  [INFERRED]
  main.py → agent/task_queue.py
- `_SleepRequested` --uses--> `JarvisUI`  [INFERRED]
  main.py → ui.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Build It Now Commercial Operating Model** — estado_maestro_producto_product_vision, about_builditnow_quality_process, build_it_legacy_90_dias_growth_plan, presupuestos_referencia_presupuesto_nuevo_2026_integral_remodel_quote [INFERRED 0.85]
- **Cortana Operational Control Loop** — estado_maestro_producto_cortana_assistant, estado_maestro_producto_hermes_runtime, cortana_command_center_command_center_prototype, memory_referencias_interfaz_cortana_command_center_ux [INFERRED 0.85]
- **Social Marketing Execution System** — investigacion_automatizacion_redes_hermes_social_publisher_gateway, investigacion_automatizacion_redes_hermes_evidence_ledger, investigacion_automatizacion_redes_hermes_meta_direct, investigacion_automatizacion_redes_hermes_grok_auditor [EXTRACTED 1.00]
- **Integrated Smart Home Systems** — mejoras_landing_smart_home_v3_uploads_sys_cinema_asset, mejoras_landing_smart_home_v3_uploads_sys_climate_asset, mejoras_landing_smart_home_v3_uploads_sys_energy_asset, mejoras_landing_smart_home_v3_uploads_sys_security_asset, mejoras_landing_smart_home_v3_uploads_sys_shading_asset, mejoras_landing_smart_home_v3_uploads_sys_surveillance_asset [INFERRED 0.95]
- **Luxury Property Lifestyle Scenarios** — mejoras_landing_smart_home_v3_uploads_final_villa_asset, mejoras_landing_smart_home_v3_uploads_hero_bedroom_asset, mejoras_landing_smart_home_v3_uploads_mood_room_asset, mejoras_landing_smart_home_v3_uploads_scn_away_asset, mejoras_landing_smart_home_v3_uploads_scn_cinema_asset [INFERRED 0.85]
- **Pool and Wellness Portfolio** — assets_piscinas_blueprint_villa_asset, assets_piscinas_col_01_infinity_asset, assets_piscinas_col_04_acrylic_asset, assets_piscinas_col_05_plunge_asset, assets_piscinas_col_06_wellness_asset, assets_piscinas_infinity_sea_asset, assets_piscinas_modern_villa_asset, assets_piscinas_pool_deck_asset, assets_piscinas_resort_pool_asset, assets_piscinas_spa_water_asset, assets_piscinas_villa_pool_asset, assets_piscinas_wel_combi_a_asset, assets_piscinas_wel_combi_b_asset [INFERRED 0.95]
- **wellness_visual_asset_collection** — assets_piscinas_wel_combi_c_jpg, assets_piscinas_wel_hammam_a_jpg, assets_piscinas_wel_hammam_b_jpg, assets_piscinas_wel_hammam_c_jpg, assets_piscinas_wel_sauna_a_jpg, assets_piscinas_wel_sauna_b_jpg, assets_piscinas_wel_sauna_c_jpg, assets_piscinas_wel_spa_a_jpg, assets_piscinas_wel_spa_b_jpg, assets_piscinas_wel_spa_c_jpg, assets_piscinas_wel_spa_d_jpg, assets_piscinas_wel_spa_e_jpg, concept_luxury_wellness [EXTRACTED 1.00]
- **smart_home_visual_asset_collection** — assets_smarthome_final_villa_jpg, assets_smarthome_hero_bedroom_jpg, assets_smarthome_mood_room_jpg, assets_smarthome_scn_arrival_jpg, assets_smarthome_scn_away_jpg, assets_smarthome_scn_cinema_jpg, assets_smarthome_scn_london_jpg, concept_smart_home [EXTRACTED 1.00]
- **home_automation_system_visual_asset_collection** — assets_smarthome_sys_cinema_jpg, assets_smarthome_sys_climate_jpg, assets_smarthome_sys_energy_jpg, assets_smarthome_sys_security_jpg, assets_smarthome_sys_shading_jpg, assets_smarthome_sys_surveillance_jpg, concept_home_automation_systems [EXTRACTED 1.00]

## Communities (64 total, 18 thin omitted)

### Community 0 - "TaskQueue"
Cohesion: 0.06
Nodes (16): _build_sandbox(), _execute_generated_code(), get_queue(), Enum, Remove terminal tasks beyond the retention limit to prevent memory leak., Task, TaskPriority, TaskQueue (+8 more)

### Community 1 - "executor.py"
Cohesion: 0.08
Nodes (43): _compare(), _ddg_search(), _format_ddg(), _gemini_search(), _get_base_dir(), Path, web_search(), youtube_video() (+35 more)

### Community 3 - "file_controller.py"
Cohesion: 0.10
Nodes (39): copy_file(), create_file(), create_folder(), delete_file(), file_controller(), find_files(), _format_size(), _get_desktop() (+31 more)

### Community 4 - "youtube_video.py"
Cohesion: 0.12
Nodes (32): _build_google_flights_url(), flight_finder(), _format_spoken(), _format_text_report(), _get_base_dir(), _parse_date(), _parse_flights_with_gemini(), Path (+24 more)

### Community 5 - "send_message.py"
Cohesion: 0.10
Nodes (27): _analyze(), _base_dir(), _capture_window(), _click_local(), _contact_fallback_query(), _contact_name_matches(), _contact_title_pattern(), _detect_visible_platform() (+19 more)

### Community 6 - "browser_control"
Cohesion: 0.14
Nodes (11): browser_control(), _BrowserThread, _ensure_started(), _find_browser_executable(), _get_default_browser_id(), _get_opera_executable(), Returns (engine_name, exe_path, channel, is_opera).     is_opera=True → extra a, Returns raw default browser identifier string for current OS. (+3 more)

### Community 7 - "game_updater.py"
Cohesion: 0.19
Nodes (27): _cancel_scheduled_update(), _click_button(), _click_first_profile_by_screenshot(), _ensure_steam_running(), _find_best_drive(), _find_epic_path(), _find_steam_path(), game_updater() (+19 more)

### Community 8 - "wake_listener.py"
Cohesion: 0.13
Nodes (22): Model, ndarray, Process, socket, WakeListenerTests, _focus_window_after_delay(), _hidden_popen(), _is_activation_clap() (+14 more)

### Community 9 - "code_helper.py"
Cohesion: 0.24
Nodes (25): _build(), _clean_code(), code_helper(), _detect_intent(), _edit_action(), _explain_action(), _fix_code(), _get_api_key() (+17 more)

### Community 10 - "computer_control.py"
Cohesion: 0.18
Nodes (25): _base_dir(), _clear_field(), _click(), _clipboard_get(), _clipboard_paste(), computer_control(), _drag(), _focus_window() (+17 more)

### Community 11 - "dev_agent.py"
Cohesion: 0.25
Nodes (20): _build_project(), _classify_error(), dev_agent(), _fix_files(), get_base_dir(), _get_model(), _has_error(), _install_dependencies() (+12 more)

### Community 12 - "screen_processor.py"
Cohesion: 0.17
Nodes (9): _capture_camera(), _capture_screenshot(), _ensure_started(), _get_api_key(), _get_camera_index(), _LiveSession, screen_process(), _to_jpeg() (+1 more)

### Community 13 - "file_processor.py"
Cohesion: 0.41
Nodes (18): _detect_type(), file_processor(), _file_size_str(), _gemini_client(), _get_api_key(), _output_path(), _process_archive(), _process_audio() (+10 more)

### Community 14 - "MainWindow"
Cohesion: 0.21
Nodes (5): QHBoxLayout, QMainWindow, QWidget, MainWindow, SetupOverlay

### Community 15 - "JarvisLive"
Cohesion: 0.20
Nodes (4): FunctionResponse, JarvisLive, Connect to Gemini Live and run until session ends or sleep is requested., Block in DORMANT state until the user presses F5 to wake Jarvis.          The

### Community 16 - "Luxury wellness offering"
Cohesion: 0.12
Nodes (17): Combined sauna and shower interior, Glass enclosed hammam, Sauna and lounge enclosure, Integrated sauna hammam spa, Outdoor poolside sauna, Luxury outdoor sauna pavilion, Freestanding sauna cabins, Garden hot tub at dusk (+9 more)

### Community 17 - "OpenRouterClient"
Cohesion: 0.20
Nodes (4): _get_base_dir(), _load_api_key(), OpenRouterClient, Path

### Community 18 - "main.py"
Cohesion: 0.19
Nodes (10): Sets a timed reminder using Windows Task Scheduler.      parameters:, reminder(), Weather report action.     Opens a Google weather search and gives a short spok, _speak_and_log(), weather_action(), _consume_startup_briefing(), _get_api_key(), _update_memory_async() (+2 more)

### Community 19 - "ui.py"
Cohesion: 0.27
Nodes (8): QColor, _base_dir(), C, _DropCanvas, _file_category(), _fmt_size(), Path, qcol()

### Community 20 - "FileDropZone"
Cohesion: 0.16
Nodes (3): QDragEnterEvent, QDropEvent, FileDropZone

### Community 21 - "desktop_control"
Cohesion: 0.33
Nodes (13): _ask_gemini_for_desktop_action(), clean_desktop(), desktop_control(), _get_base_dir(), get_current_wallpaper(), _get_desktop(), get_desktop_stats(), list_desktop() (+5 more)

### Community 22 - "Cortana Assistant Layer"
Cohesion: 0.14
Nodes (14): Build It Legacy 90-Day Plan, Cortana Command Center Prototype, Commercial Architecture, Cortana Assistant Layer, Hermes Runtime, Product Vision, Social Automation Feasibility Query, Append-only Evidence Ledger (+6 more)

### Community 23 - "memory_manager.py"
Cohesion: 0.28
Nodes (12): _all_entries(), _empty_memory(), forget(), get_base_dir(), load_memory(), Path, _recursive_update(), remember() (+4 more)

### Community 25 - "JarvisUI"
Cohesion: 0.20
Nodes (3): main(), JarvisUI, F5: toggle between dormant and active. Calls on_wake_requested if set.

### Community 26 - "config_manager.py"
Cohesion: 0.31
Nodes (7): ensure_config_dir(), get_base_dir(), get_gemini_key(), is_configured(), load_api_keys(), Path, save_api_keys()

### Community 27 - "computer_settings"
Cohesion: 0.25
Nodes (8): computer_settings(), _detect_action(), press_key(), refresh_page(), reload_page_n(), scroll_down(), scroll_up(), volume_set()

### Community 28 - "Smart home offering"
Cohesion: 0.25
Nodes (8): Modern smart-home villa exterior, Luxury bedroom interior, Ambient living room, Private jet arrival scenario, Away mode villa scenario, Home cinema scenario, London city scenario, Smart home offering

### Community 30 - "_SysMetrics"
Cohesion: 0.39
Nodes (3): Run a HUD metrics probe without flashing a console window on Windows., _run_background(), _SysMetrics

### Community 32 - "Home automation systems"
Cohesion: 0.29
Nodes (7): Home cinema system, Climate-controlled living space, Solar energy system, Smart lock security system, Motorized shading system, Surveillance camera system, Home automation systems

### Community 34 - "Build It Now Quality Process"
Cohesion: 0.33
Nodes (6): Build It Now Quality Process, Premium Pools Offer, Smart Home Offer, Build It Now Brand Standard, 2025 Kitchen Quote, 2026 Integral Renovation Quote

### Community 36 - "_SleepRequested"
Cohesion: 0.40
Nodes (4): Exception, Polls _sleep_requested and raises _SleepRequested to cancel the session., Raised from _watch_sleep to cancel the active Gemini session gracefully., _SleepRequested

### Community 37 - "Modern Tropical Villa Exterior"
Cohesion: 0.40
Nodes (5): Modern Tropical Villa Exterior, Luxury Bedroom Interior, Contemporary Living Room Interior, Luxury Villa Away Scene, Solar Energy Installation

### Community 38 - "Build It Now BlueLiving Partner Campaign"
Cohesion: 0.50
Nodes (4): BlueLiving Wellness Campaign, Build It Now BlueLiving Partner Campaign, Infinity and Wellness Offer, BlueLiving Advertising Materials

### Community 39 - "._build_config"
Cohesion: 0.50
Nodes (3): LiveConnectConfig, _load_system_prompt(), format_memory_for_prompt()

### Community 41 - "type_text"
Cohesion: 0.67
Nodes (3): copy(), paste(), type_text()

### Community 42 - "Modern Villa Pool Exterior"
Cohesion: 0.67
Nodes (3): Villa and Pool Architectural Blueprint, Modern Villa Pool Exterior, Modern White Villa Pool

### Community 43 - "Ocean View Infinity Pool Villa"
Cohesion: 0.67
Nodes (3): Ocean View Infinity Pool Villa, Acrylic Wall Pool Villa, Tropical Resort Infinity Pool

### Community 44 - "Luxury Spa and Hydrotherapy Room"
Cohesion: 0.67
Nodes (3): Wellness Pool and Outdoor Lounge, Glass Sauna and Wellness Room, Luxury Spa and Hydrotherapy Room

### Community 45 - "MARK XXXIX-OR Upstream Assistant"
Cohesion: 0.67
Nodes (3): Jarvis Predator Reference, MARK XXXIX-OR Upstream Assistant, Jarvis Runtime Stack

### Community 46 - "Integrated Climate Control Interior"
Cohesion: 0.67
Nodes (3): Climate Control Storytelling Panel, Integrated Climate Control Interior, Bedroom Automated Shading Interior

### Community 47 - "Smart Lock Access Control"
Cohesion: 0.67
Nodes (3): Smart Access Security Storytelling Panel, Smart Lock Access Control, Security Surveillance Camera

## Ambiguous Edges - Review These
- `London city scenario` → `Smart home offering`  [AMBIGUOUS]
  assets-smarthome/scn-london.jpg · relation: supports_lifestyle_scenario

## Knowledge Gaps
- **69 isolated node(s):** `C`, `Commercial Architecture`, `Meta Direct Adapter`, `Grok Bot Auditor`, `BlueLiving Wellness Campaign` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `London city scenario` and `Smart home offering`?**
  _Edge tagged AMBIGUOUS (relation: supports_lifestyle_scenario) - confidence is low._
- **Why does `TaskPriority` connect `TaskQueue` to `executor.py`, `main.py`, `_SleepRequested`, `JarvisLive`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `file_controller()` connect `file_controller.py` to `executor.py`, `main.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `JarvisLive` connect `JarvisLive` to `TaskQueue`, `executor.py`, `_SleepRequested`, `._build_config`, `main.py`, `JarvisUI`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `JarvisLive` (e.g. with `TaskPriority` and `JarvisUI`) actually correct?**
  _`JarvisLive` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `C`, `Commercial Architecture`, `Meta Direct Adapter` to the rest of the system?**
  _69 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `TaskQueue` be split into smaller, more focused modules?**
  _Cohesion score 0.06397306397306397 - nodes in this community are weakly interconnected._