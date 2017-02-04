# Fashion Recommend Engine's API Server

## Dependencies

```bash
$ pip install flask flask-uploads
```

## Run

```bash
$ python3 server.py
```

## 画像を解析(男性)

```
POST /reco/men

image - Self photo
```

### レスポンス

```json
{
  "cluster": number,
  "skin_color": string,
  "hair_color": string,
  "ratio": float,
  "contour": number,
  "colors": [
    {"outer": string, "inner": string, "bottom": string},
  ],
  "clothes": [
    {"outer": string, "inner": string, "bottom": string},
  ]
}
```

## 画像を解析(女性)

```
POST /reco/women

image - Self photo
```