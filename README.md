SkyTorque UAV Software

Bu repo, quadcopter tabanlı otonom İHA yazılım geliştirme sürecini içermektedir.
Projede kullanılan yapı:

PX4 SITL

Gazebo Sim

QGroundControl

Python tabanlı onboard görev yazılımı

MAVLink haberleşmesi

Bu yapı sayesinde gerçek donanıma geçmeden önce simülasyon ortamında:

bağlantı testi

arm / disarm

takeoff / landing

görev durum makinesi

telemetri takibi

gibi işlemler test edilebilmektedir.

Kullanılan Mimari

Gerçek sistem

Pixhawk 6C → uçuş kontrol

Raspberry Pi 4 → görev yönetimi ve görüntü işleme

Simülasyon sistemi

PX4 SITL → sanal uçuş kontrolcüsü

Gazebo → fiziksel simülasyon

QGroundControl → yer istasyonu

Python kodu → görev yazılımı

Proje Yapısı
skytorque-uav-software/
│
├── README.md
├── requirements.txt
├── config/
│   └── mission.yaml
├── docs/
├── onboard/
│   ├── main.py
│   ├── test_arm.py
│   ├── test_disarm.py
│   ├── test_mini_mission.py
│   ├── test_takeoff.py
│   ├── ARMING
│   ├── COMPLETE
│   ├── HOLD
│   ├── LANDING
│   ├── TAKEOFF
│   ├── mavlink_bridge/
│   │   └── px4_interface.py
│   └── mission_manager/
│       └── state_machine.py
├── simulation/
│   ├── gazebo_world/
│   └── px4_sitl/
├── tests/
│   ├── test_px4_raw_messages.py
│   ├── tests_px4_connection.py
│   └── tests_px4_telemetry.py
└── tools/

docs/: Dokümantasyon dosyaları

simulation/: Simülasyon ortamı dosyaları

tests/: Test scriptleri

tools/: Yardımcı araçlar

Gereksinimler

Aşağıdaki yazılımların kurulu olması gerekir:

PX4-Autopilot

Gazebo Sim

QGroundControl

Python 3

pymavlink

Python bağımlılığı kurulumu:

pip install -r requirements.txt
PX4 SITL ve Gazebo Çalıştırma

Önce PX4 simülasyonu başlatılır:

cd ~/code/PX4-Autopilot
make px4_sitl gz_x500

Bu komut:

PX4 SITL’i başlatır

Gazebo simülasyonunu açar

x500 drone modelini spawn eder

QGroundControl Çalıştırma

QGroundControl ayrı bir terminalden açılır:

cd ~/Downloads
./QGroundControl-x86_64.AppImage

QGroundControl açıldıktan sonra araç otomatik olarak bağlanmalıdır.

Bağlantı başarılıysa:

araç haritada görünür

durum kısmında Ready To Fly yazısı görülür

Python Görev Yazılımını Çalıştırma

Onboard yazılım klasörüne geçilir:

cd ~/code/skytorque-uav-software/onboard

Ana görev akışını çalıştırmak için:

python3 main.py

Bu script aşağıdaki görev akışını uygular:

INIT
→ ARMING
→ TAKEOFF
→ HOLD
→ LANDING
→ COMPLETE
Test Scriptleri
1. Disarm testi
python3 test_disarm.py

Araç disarm durumuna alınır.

2. Arm testi
python3 test_arm.py

Araç arm edilir ve heartbeat üzerinden kontrol edilir.

3. Takeoff testi
python3 test_takeoff.py

Araç hedef irtifaya kalkar ve irtifa bilgisi terminalde izlenir.

4. Mini mission testi
python3 test_mini_mission.py

Küçük bir görev akışı test edilir.

MAVLink Bağlantı Bilgisi

Python görev yazılımı PX4’e şu bağlantı üzerinden bağlanır:

udpin:0.0.0.0:14540

Bu port PX4’ün onboard MAVLink çıkışına karşılık gelir.