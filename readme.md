# PDF Enumerator

## Как установить зависимости
```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

## Как запустить программу

```python
...
if __name__ == "__main__":
    pdf_enumerator = PdfEnumerator("C:/Users/Катя/Desktop/pdf_enumerator/") # Тут указать путь до папки c pdf или список с несколькими папками
    pdf_enumerator.main()
```


```bash
python pdf_enumerator.py
```
