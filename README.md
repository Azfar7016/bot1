# Clavaria Helper Discord Bot

[![Discord server](https://img.shields.io/discord/984083803796561960?label=Join%20our%20Discord%20Server%21)](https://discord.gg/d4RCAhwAMr) [![Build Production](https://github.com/GNZTMPZ/BOT-CLAVARIA/actions/workflows/build.yml/badge.svg)](https://github.com/GNZTMPZ/BOT-CLAVARIA/actions/workflows/build.yml) [![precommit-action](https://github.com/GNZTMPZ/BOT-CLAVARIA/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/GNZTMPZ/BOT-CLAVARIA/actions/workflows/pre-commit.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Clavaria Roleplay Discord Server Bots & UCP System made with [NAFF](https://github.com/NAFTeam/NAFF).

Kunjungi [panduan resmi NAFF](https://naff.info/Guides/01%20Getting%20Started.html) untuk memulai.

#### Note:

Tidak disarankan untuk menjalankan repository ini secara langsung tanpa merubah codingan apapun (walaupun repository ini sudah Production Ready) karena repository ini telah didesign khusus hanya untuk Clavaria Roleplay. Repository ini dibuat publik hanya untuk media belajar/referensi.

## Menjalankan Aplikasi

Ada beberapa cara untuk menjalankan aplikasi ini.

### Docker

Repository ini sudah _Docker Ready_, anda hanya tinggal meng-pull container nya. Cek selengkapnya di [halaman ini!](https://github.com/GNZTMPZ/BOT-CLAVARIA/pkgs/container/bot-clavaria)

- Pastikan Docker anda sudah terinstall versi terbaru!
- Anda hanya butuh menjalankan command:

```bash
docker-compose up --detach
```

### Manual Install

- Download dan install Python versi terbaru (usahakan yg terbaru, jangan yang jadul)

**WAJIB PAKE `virtualenv`, Please check python docs for more info!**

```md
saya anggap kalian sudah setup "virtualenv"
```

- Install dependencies package nya menggunakan perintah ini

```bash
pip install -r ".\requirements.txt"
```

- sebelum menjalankan kode ini, buatlah satu file `.env` di folder root dan isi filenya menggunakan contoh berikut

```env
PROJECT_NAME="Clavaria Helper"
LOAD_DEBUG_COMMANDS=true # untuk production ready, ganti value ini ke false
DISCORD_TOKEN="masukkan bot token anda disini, ambil di https://discord.com/developers/applications"
DATABASE_HOST="masukkan mysql database host kamu disini"
DATABASE_USER="masukkan username mysql kamu disini"
DATABASE_PASSWORD="masukkan password mysql kamu disini"
DATABASE_NAME="masukkan nama mysql database kamu disini"
IP="ip server kamu, support domain dan ip"
PORT="port server samp kamu"
```

- anda sudah siap menjalankan botnya. untuk menjalankan botnya, gunakan perintah ini

```bash
py main.py
```

## Informasi Tambahan
Kami sudah siapkan konfigurasi [pre-commit](https://pre-commit.com) bawaan untuk merapihkan kodingan kalian.

Sangat direkomendasikan untuk menggunakan tool ini dengan menjalankan perintah berikut:

1) `pip install pre-commit`
2) `pre-commit install`

## License

Seluruh source code ini menggunakan lisensi GNU GPL 2.0, Mohon mencantumkan Copyright notice saat anda menggunakan code ini!

Copyright ©️2022 Clemie McCartney ([Sanity#0007](https://discord.com/users/351150966948757504)). Licensed to Clavaria Roleplay.
