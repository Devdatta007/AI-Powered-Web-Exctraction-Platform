import io
import time
import zipfile
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader

app = FastAPI(title="Stitch — AI Web Extraction Platform")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

task_history: list[dict] = []


# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_soup(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return BeautifulSoup(r.content, "html.parser"), ""
    except Exception as e:
        return None, str(e)


def extract_links(soup: BeautifulSoup, base_url: str) -> list:
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        full = urljoin(base_url, href)
        if full.startswith("http") and full not in links:
            links.append(full)
    return links


def extract_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def extract_pdf_text(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        reader = PdfReader(io.BytesIO(r.content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip(), ""
    except Exception as e:
        return "", str(e)


def collect_pdf_urls(soup: BeautifulSoup, base_url: str) -> list:
    return [
        urljoin(base_url, a["href"])
        for a in soup.find_all("a", href=True)
        if a["href"].lower().endswith(".pdf")
    ]


def collect_image_urls(soup: BeautifulSoup, base_url: str) -> list:
    exts = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp")
    urls = []
    for tag in soup.find_all(["img", "a"]):
        src = tag.get("src") or tag.get("href") or ""
        if src.lower().endswith(exts):
            full = urljoin(base_url, src)
            if full not in urls:
                urls.append(full)
    return urls


def record_task(url: str, mode: str, status: str, detail: str = ""):
    task_history.append({
        "id": f"#{len(task_history) + 1001}",
        "url": url,
        "mode": mode,
        "status": status,
        "detail": detail,
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


# ── Pages ─────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "history": task_history[-10:][::-1]}
    )


@app.get("/new-task", response_class=HTMLResponse)
async def new_task_page(request: Request):
    return templates.TemplateResponse("new_task.html", {"request": request})


@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    total = len(task_history)
    success = sum(1 for t in task_history if t["status"] == "success")
    rate = round((success / total * 100), 1) if total else 0
    return templates.TemplateResponse(
        "analytics.html",
        {"request": request, "total": total, "success": success, "rate": rate,
         "history": task_history[-20:][::-1]},
    )


@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    return templates.TemplateResponse(
        "results.html", {"request": request, "history": task_history[-20:][::-1]}
    )


# ── Scraping API endpoints ────────────────────────────────────────────────────

@app.post("/api/extract/links")
async def api_extract_links(url: str = Form(...)):
    t0 = time.time()
    soup, err = fetch_soup(url)
    if err:
        record_task(url, "Embedded Links", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    links = extract_links(soup, url)
    elapsed = round(time.time() - t0, 2)
    record_task(url, "Embedded Links", "success", f"{len(links)} links found")
    return {"url": url, "mode": "Embedded Links", "count": len(links),
            "elapsed": elapsed, "data": links}


@app.post("/api/extract/text")
async def api_extract_text(url: str = Form(...)):
    t0 = time.time()
    soup, err = fetch_soup(url)
    if err:
        record_task(url, "Main Text", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    text = extract_text(soup)
    elapsed = round(time.time() - t0, 2)
    record_task(url, "Main Text", "success", f"{len(text)} chars")
    return {"url": url, "mode": "Main Text", "elapsed": elapsed, "data": text}


@app.post("/api/extract/text-with-links")
async def api_text_with_links(url: str = Form(...)):
    t0 = time.time()
    soup, err = fetch_soup(url)
    if err:
        record_task(url, "Text + Links Text", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    main_text = extract_text(soup)
    links = extract_links(soup, url)
    combined = main_text + "\n\n--- LINKED PAGES ---\n"
    for link in links[:10]:
        s2, _ = fetch_soup(link)
        if s2:
            combined += f"\n[{link}]\n{extract_text(s2)}\n"
    elapsed = round(time.time() - t0, 2)
    record_task(url, "Text + Links Text", "success", f"{len(links)} links crawled")
    return {"url": url, "mode": "Text + Links Text", "elapsed": elapsed, "data": combined}


@app.post("/api/extract/complete-text")
async def api_complete_text(url: str = Form(...)):
    t0 = time.time()
    soup, err = fetch_soup(url)
    if err:
        record_task(url, "Complete Text", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    links = extract_links(soup, url)
    all_text = f"[{url}]\n{extract_text(soup)}\n"
    for link in links[:20]:
        s2, _ = fetch_soup(link)
        if s2:
            all_text += f"\n[{link}]\n{extract_text(s2)}\n"
    elapsed = round(time.time() - t0, 2)
    record_task(url, "Complete Text", "success", f"{len(links)} pages")
    return {"url": url, "mode": "Complete Text", "elapsed": elapsed, "data": all_text}


@app.post("/api/extract/pdf-text")
async def api_pdf_text(url: str = Form(...)):
    t0 = time.time()
    text, err = extract_pdf_text(url)
    if err:
        record_task(url, "PDF Text", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    elapsed = round(time.time() - t0, 2)
    record_task(url, "PDF Text", "success", f"{len(text)} chars")
    return {"url": url, "mode": "PDF Text", "elapsed": elapsed, "data": text}


@app.post("/api/extract/pdf-with-links")
async def api_pdf_with_links(url: str = Form(...)):
    t0 = time.time()
    soup, err = fetch_soup(url)
    if err:
        record_task(url, "PDF + Links PDF", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    pdf_urls = collect_pdf_urls(soup, url)
    combined = ""
    for pu in pdf_urls[:10]:
        txt, _ = extract_pdf_text(pu)
        combined += f"\n[{pu}]\n{txt}\n"
    elapsed = round(time.time() - t0, 2)
    record_task(url, "PDF + Links PDF", "success", f"{len(pdf_urls)} PDFs")
    return {"url": url, "mode": "PDF + Links PDF", "elapsed": elapsed,
            "count": len(pdf_urls), "data": combined}


@app.post("/api/extract/complete-pdf")
async def api_complete_pdf(url: str = Form(...)):
    t0 = time.time()
    soup, err = fetch_soup(url)
    if err:
        record_task(url, "Complete PDF", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    links = extract_links(soup, url)
    all_pdfs = collect_pdf_urls(soup, url)
    for link in links[:15]:
        s2, _ = fetch_soup(link)
        if s2:
            all_pdfs += collect_pdf_urls(s2, link)
    all_pdfs = list(dict.fromkeys(all_pdfs))
    combined = ""
    for pu in all_pdfs[:20]:
        txt, _ = extract_pdf_text(pu)
        combined += f"\n[{pu}]\n{txt}\n"
    elapsed = round(time.time() - t0, 2)
    record_task(url, "Complete PDF", "success", f"{len(all_pdfs)} PDFs")
    return {"url": url, "mode": "Complete PDF", "elapsed": elapsed,
            "count": len(all_pdfs), "data": combined}


@app.post("/api/extract/complete-text-pdf")
async def api_complete_text_pdf(url: str = Form(...)):
    t0 = time.time()
    soup, err = fetch_soup(url)
    if err:
        record_task(url, "Text + PDF", "error", err)
        return JSONResponse({"error": err}, status_code=400)
    text = extract_text(soup)
    pdf_urls = collect_pdf_urls(soup, url)
    pdf_text = ""
    for pu in pdf_urls[:10]:
        t, _ = extract_pdf_text(pu)
        pdf_text += f"\n[{pu}]\n{t}\n"
    elapsed = round(time.time() - t0, 2)
    record_task(url, "Text + PDF", "success", f"{len(pdf_urls)} PDFs")
    return {"url": url, "mode": "Text + PDF", "elapsed": elapsed,
            "data": text + "\n\n--- PDF DATA ---\n" + pdf_text}


@app.post("/api/download/pdfs")
async def api_download_pdfs(url: str = Form(...)):
    soup, err = fetch_soup(url)
    if err:
        return JSONResponse({"error": err}, status_code=400)
    pdf_urls = collect_pdf_urls(soup, url)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for pu in pdf_urls[:20]:
            try:
                r = requests.get(pu, headers=HEADERS, timeout=15)
                name = urlparse(pu).path.split("/")[-1] or "file.pdf"
                zf.writestr(name, r.content)
            except Exception:
                pass
    buf.seek(0)
    record_task(url, "Download PDFs", "success", f"{len(pdf_urls)} PDFs zipped")
    return StreamingResponse(buf, media_type="application/zip",
                             headers={"Content-Disposition": "attachment; filename=pdfs.zip"})


@app.post("/api/download/all-pdfs")
async def api_download_all_pdfs(url: str = Form(...)):
    soup, err = fetch_soup(url)
    if err:
        return JSONResponse({"error": err}, status_code=400)
    links = extract_links(soup, url)
    all_pdfs = collect_pdf_urls(soup, url)
    for link in links[:15]:
        s2, _ = fetch_soup(link)
        if s2:
            all_pdfs += collect_pdf_urls(s2, link)
    all_pdfs = list(dict.fromkeys(all_pdfs))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for pu in all_pdfs[:30]:
            try:
                r = requests.get(pu, headers=HEADERS, timeout=15)
                name = urlparse(pu).path.split("/")[-1] or "file.pdf"
                zf.writestr(name, r.content)
            except Exception:
                pass
    buf.seek(0)
    record_task(url, "Download All PDFs", "success", f"{len(all_pdfs)} PDFs zipped")
    return StreamingResponse(buf, media_type="application/zip",
                             headers={"Content-Disposition": "attachment; filename=all_pdfs.zip"})


@app.post("/api/download/images")
async def api_download_images(url: str = Form(...)):
    soup, err = fetch_soup(url)
    if err:
        return JSONResponse({"error": err}, status_code=400)
    img_urls = collect_image_urls(soup, url)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for iu in img_urls[:30]:
            try:
                r = requests.get(iu, headers=HEADERS, timeout=15)
                name = urlparse(iu).path.split("/")[-1] or "image.jpg"
                zf.writestr(name, r.content)
            except Exception:
                pass
    buf.seek(0)
    record_task(url, "Download Images", "success", f"{len(img_urls)} images zipped")
    return StreamingResponse(buf, media_type="application/zip",
                             headers={"Content-Disposition": "attachment; filename=images.zip"})


@app.post("/api/download/all-images")
async def api_download_all_images(url: str = Form(...)):
    soup, err = fetch_soup(url)
    if err:
        return JSONResponse({"error": err}, status_code=400)
    links = extract_links(soup, url)
    all_imgs = collect_image_urls(soup, url)
    for link in links[:15]:
        s2, _ = fetch_soup(link)
        if s2:
            all_imgs += collect_image_urls(s2, link)
    all_imgs = list(dict.fromkeys(all_imgs))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for iu in all_imgs[:50]:
            try:
                r = requests.get(iu, headers=HEADERS, timeout=15)
                name = urlparse(iu).path.split("/")[-1] or "image.jpg"
                zf.writestr(name, r.content)
            except Exception:
                pass
    buf.seek(0)
    record_task(url, "Download All Images", "success", f"{len(all_imgs)} images zipped")
    return StreamingResponse(buf, media_type="application/zip",
                             headers={"Content-Disposition": "attachment; filename=all_images.zip"})


@app.get("/api/history")
async def api_history():
    return {"tasks": task_history[::-1]}
