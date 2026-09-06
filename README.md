# Thai Provinces API

REST API สำหรับข้อมูลที่อยู่ประเทศไทยครบ 77 จังหวัด พร้อมอำเภอ/เขต ตำบล/แขวง และรหัสไปรษณีย์ ใช้ JSON ที่ validate แล้วเป็น data source จึงไม่เรียก external API ระหว่างรับ request

## Features

- จังหวัด 77 จังหวัด, 928 อำเภอ และ 7,436 ตำบล
- FastAPI + Pydantic v2 พร้อม OpenAPI, Swagger UI และ ReDoc
- ค้นหาด้วยรหัสไปรษณีย์แบบ string 5 หลัก
- Repository layer และ cached file loading
- Deploy เป็น Vercel Serverless Function ได้

## Technology Stack

Python 3.11+, FastAPI, Pydantic v2, Uvicorn, pytest, JSON และ Vercel

## Project Structure

```text
app/
	api/routes.py
	data/data.json
	repositories/province_repository.py
	dependencies.py
	models.py
scripts/generate_data.py
tests/
main.py
vercel.json
```

## Requirements and Installation

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Generate Complete Data

ข้อมูลที่ commit ใน `app/data/data.json` สร้างจาก [Thailand Geography JSON](https://github.com/thailand-geography-data/thailand-geography-json) โดย generator จะตรวจจำนวนจังหวัด, foreign keys, duplicate IDs, postal codes และขนาดข้อมูลก่อนเขียนไฟล์

```bash
python scripts/generate_data.py
```

หลังจากสร้างไฟล์แล้ว API ทำงานแบบ offline ได้ และไม่จำเป็นต้องเชื่อมต่ออินเทอร์เน็ตขณะรับ request

## Run Locally

```bash
uvicorn main:app --reload
```

เปิด `http://127.0.0.1:8000/docs` สำหรับ Swagger UI, `http://127.0.0.1:8000/redoc` สำหรับ ReDoc และ `http://127.0.0.1:8000/openapi.json` สำหรับ OpenAPI JSON

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/provinces` | รายชื่อจังหวัดทั้งหมด |
| GET | `/api/provinces/{province_id}/districts` | อำเภอ/เขตในจังหวัด |
| GET | `/api/districts/{district_id}/subdistricts` | ตำบล/แขวงและรหัสไปรษณีย์ |
| GET | `/api/search?zipcode=10400` | ค้นหาที่อยู่ตามรหัสไปรษณีย์ |
| GET | `/health` | ตรวจสอบสถานะระบบ |

ตัวอย่าง:

```bash
curl http://127.0.0.1:8000/api/provinces
curl http://127.0.0.1:8000/api/provinces/10/districts
curl http://127.0.0.1:8000/api/districts/1001/subdistricts
curl 'http://127.0.0.1:8000/api/search?zipcode=10400'
curl http://127.0.0.1:8000/health
```

รหัสจังหวัด/อำเภอที่ไม่มีอยู่และ zipcode ที่ไม่พบตอบ `404`; zipcode ที่ไม่ใช่ตัวเลข 5 หลักตอบ `422`

## Tests

```bash
pytest -v
```

## Deploy to Vercel

```bash
npm install -g vercel
vercel login
vercel
vercel --prod
```

`vercel.json` ใช้ `main.py` เป็น entry point และ data file อยู่ใน source tree จึงถูก bundle ไปพร้อม Serverless Function โดยใช้ path ที่อิงจาก `__file__`

## CORS Security

ค่าเริ่มต้นเปิดทุก origin ตามโจทย์ (`allow_origins=["*"]`) และปิด credentials หาก Production ต้องใช้ Cookie หรือ cross-origin credentials ควรเปลี่ยน wildcard เป็นรายการโดเมนที่อนุญาตอย่างชัดเจน

## Data Source and Attribution

ข้อมูลมาจาก [thailand-geography-json](https://github.com/thailand-geography-data/thailand-geography-json) โดย Thailand Geography Data ซึ่งเผยแพร่ภายใต้ MIT License โปรดตรวจสอบ source และ license ล่าสุดก่อนนำไปใช้เชิงพาณิชย์หรือ redistribute

## License

โค้ดโปรเจกต์นี้เผยแพร่ภายใต้ MIT License ดูรายละเอียดใน [LICENSE](LICENSE) และเปลี่ยน `<YOUR_NAME>` เป็นชื่อเจ้าของลิขสิทธิ์ก่อนเผยแพร่

## Contributing

เปิด issue หรือ pull request พร้อมคำอธิบายการเปลี่ยนแปลงและผลการรัน `pytest -v` ข้อมูลที่แก้ไขควรสร้างผ่าน `scripts/generate_data.py` และต้องผ่าน validation ทุกครั้ง
# Thai-Provinces-API