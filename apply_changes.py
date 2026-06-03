import os

file_path = "../sovi-20-questions-demo/pictures/generate_characters.py"

if not os.path.exists(file_path):
    print("Error: Target file not found!")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Replace upload_to_r2
old_upload_to_r2 = """def upload_to_r2(local_path, r2_key):
    \"\"\"Uploads a local file to Cloudflare R2 bucket using wrangler CLI.\"\"\"
    cmd = f'npx wrangler r2 object put "{R2_BUCKET}/{r2_key}" --file "{local_path}"'
    success, output = run_cmd(cmd)
    if not success:
        print(f"  [R2 Upload Failed] {r2_key}: {output}")
    return success"""

new_upload_to_r2 = """def upload_to_r2(local_path, r2_key, logger=None):
    \"\"\"Uploads a local file to Cloudflare R2 bucket using wrangler CLI.\"\"\"
    cmd = f'npx wrangler r2 object put "{R2_BUCKET}/{r2_key}" --file "{local_path}"'
    success, output = run_cmd(cmd)
    if not success:
        msg = f"  [R2 Upload Failed] {r2_key}: {output}"
        if logger:
            logger(msg)
        else:
            print(msg)
    return success"""

# 2. Replace write_to_kv
old_write_to_kv = """def write_to_kv(key, json_val):
    \"\"\"Writes JSON metadata to Cloudflare KV namespace using wrangler CLI via a temp file.\"\"\"
    json_str = json.dumps(json_val, ensure_ascii=False)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(json_str)
        temp_path = f.name
    try:
        cmd = f'npx wrangler kv:key put --namespace-id {KV_NAMESPACE_ID} "{key}" --file "{temp_path}"'
        success, output = run_cmd(cmd)
        if not success:
            print(f"  [KV Write Failed] {key}: {output}")
        return success
    finally:
        try:
            os.unlink(temp_path)
        except Exception:
            pass"""

new_write_to_kv = """def write_to_kv(key, json_val, logger=None):
    \"\"\"Writes JSON metadata to Cloudflare KV namespace using wrangler CLI via a temp file.\"\"\"
    json_str = json.dumps(json_val, ensure_ascii=False)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(json_str)
        temp_path = f.name
    try:
        cmd = f'npx wrangler kv:key put --namespace-id {KV_NAMESPACE_ID} "{key}" --file "{temp_path}"'
        success, output = run_cmd(cmd)
        if not success:
            msg = f"  [KV Write Failed] {key}: {output}"
            if logger:
                logger(msg)
            else:
                print(msg)
        return success
    finally:
        try:
            os.unlink(temp_path)
        except Exception:
            pass"""

# 3. Replace compress_image
old_compress_image = """def compress_image(input_path, output_path, max_size_kb=300):
    \"\"\"Compresses a PNG image to a JPEG under max_size_kb using Pillow.\"\"\"
    try:
        from PIL import Image
        with Image.open(input_path) as img:
            # Convert RGBA/P to RGB with white background
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                mask = img.split()[3] if img.mode == 'RGBA' else None
                bg.paste(img, mask=mask)
                img = bg
            else:
                img = img.convert('RGB')

            # Save as JPEG with quality 85 and optimization
            img.save(output_path, "JPEG", quality=85, optimize=True)

            # Check size and re-compress with lower quality if needed
            size_kb = os.path.getsize(output_path) / 1024
            if size_kb > max_size_kb:
                img.save(output_path, "JPEG", quality=65, optimize=True)

            final_size = os.path.getsize(output_path) / 1024
            print(f"  [Compression] Compressed image from {os.path.getsize(input_path)/1024:.1f}KB to {final_size:.1f}KB")
            return True
    except ImportError:
        print("  [Notice] PIL (Pillow) is not installed. To compress images under 300KB, please run: pip install Pillow")
        import shutil
        try:
            shutil.copy(input_path, output_path)
            return True
        except Exception as e:
            print(f"  [Error] Failed to copy fallback image: {e}")
            return False
    except Exception as e:
        print(f"  [Error] Failed to compress image: {e}")
        return False"""

new_compress_image = """def compress_image(input_path, output_path, max_size_kb=300, logger=None):
    \"\"\"Compresses a PNG image to a JPEG under max_size_kb using Pillow.\"\"\"
    try:
        from PIL import Image
        with Image.open(input_path) as img:
            # Convert RGBA/P to RGB with white background
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                mask = img.split()[3] if img.mode == 'RGBA' else None
                bg.paste(img, mask=mask)
                img = bg
            else:
                img = img.convert('RGB')

            # Save as JPEG with quality 85 and optimization
            img.save(output_path, "JPEG", quality=85, optimize=True)

            # Check size and re-compress with lower quality if needed
            size_kb = os.path.getsize(output_path) / 1024
            if size_kb > max_size_kb:
                img.save(output_path, "JPEG", quality=65, optimize=True)

            final_size = os.path.getsize(output_path) / 1024
            msg = f"  [Compression] Compressed image from {os.path.getsize(input_path)/1024:.1f}KB to {final_size:.1f}KB"
            if logger:
                logger(msg)
            else:
                print(msg)
            return True
    except ImportError:
        msg_notice = "  [Notice] PIL (Pillow) is not installed. To compress images under 300KB, please run: pip install Pillow"
        if logger:
            logger(msg_notice)
        else:
            print(msg_notice)
        import shutil
        try:
            shutil.copy(input_path, output_path)
            return True
        except Exception as e:
            msg_fail = f"  [Error] Failed to copy fallback image: {e}"
            if logger:
                logger(msg_fail)
            else:
                print(msg_fail)
            return False
    except Exception as e:
        msg_err = f"  [Error] Failed to compress image: {e}"
        if logger:
            logger(msg_err)
        else:
            print(msg_err)
        return False"""

# 4. Replace process_character_row completely
# Let's locate process_character_row definition start and find its end
start_keyword = "def process_character_row(row, api_key):"
end_keyword = "def save_progress("

idx_start = code.find(start_keyword)
idx_end = code.find(end_keyword)

if idx_start == -1 or idx_end == -1:
    print("Error: Could not locate process_character_row in the code!")
    exit(1)

# Grab original code block
original_process_block = code[idx_start:idx_end]

# Let's form the new process_character_row block
new_process_block = """def process_character_row(row, api_key):
    category = row.get("分类", "General")
    en_name = row.get("英文名字", "").strip()
    zh_name = row.get("中文名字", "").strip()

    if not en_name or not zh_name:
        return None

    # Check cache first
    en_hash = sha256(tcg_hash_input(en_name, "en"))
    zh_hash = sha256(tcg_hash_input(zh_name, "zh"))

    with file_lock:
        try:
            with open(JSON_CACHE_PATH, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    # If already generated both completely, skip!
    if en_hash in cache and zh_hash in cache:
        print(f"  [Skipping] {en_name} / {zh_name} (Already pre-generated)")
        return "skipped"

    # Initialize a local logs buffer to keep outputs atomic and non-interleaved
    local_logs = []
    def log(msg):
        local_logs.append(msg)

    log(f"\\n>>> Generating: {en_name} / {zh_name} (Category: {category})...")

    try:
        # Generate English metadata first
        log("  [1/4] Generating English Card Metadata...")
        en_data = generate_metadata_text(en_name, "en", api_key)
        en_prompt = character_art_prompt(en_name, en_data.get("imagePrompt"))

        # Generate Chinese metadata
        log("  [2/4] Generating Chinese Card Metadata...")
        zh_data = generate_metadata_text(zh_name, "zh", api_key)

        # Generate the IMAGE once (using the English prompt for maximum quality)
        log(f"  [3/4] Calling Image Generation API with prompt: {en_prompt[:60]}...")
        img_ref = generate_image_url(en_prompt, api_key)

        # Save original image locally using English hash
        local_orig_name = f"tcg_img_{en_hash}_orig.png"
        local_orig_path = os.path.join(LOCAL_IMAGES_DIR, local_orig_name)
        download_image(img_ref, local_orig_path)
        log(f"  Saved original image locally to: {local_orig_path}")

        # Generate compressed image
        local_thumb_name = f"tcg_img_{en_hash}_thumb.jpg"
        local_thumb_path = os.path.join(LOCAL_IMAGES_DIR, local_thumb_name)
        compress_image(local_orig_path, local_thumb_path, logger=log)

        # Upload original image to Cloudflare R2
        r2_orig_key = f"{R2_PREFIX}/{local_orig_name}"
        log(f"  [4/4] Uploading original image to Cloudflare R2: {r2_orig_key}...")
        orig_upload_success = upload_to_r2(local_orig_path, r2_orig_key, logger=log)

        # Upload compressed thumbnail image to Cloudflare R2
        r2_thumb_key = f"{R2_PREFIX}/{local_thumb_name}"
        log(f"  Uploading compressed thumbnail to Cloudflare R2: {r2_thumb_key}...")
        thumb_upload_success = upload_to_r2(local_thumb_path, r2_thumb_key, logger=log)

        if thumb_upload_success:
            r2_thumb_url = f"https://sovi-static-files.mysovi.ai/{r2_thumb_key}"
        else:
            # Fallback to original URL or local assets
            r2_thumb_url = img_ref if not img_ref.startswith("data:") else f"/assets/{local_thumb_name}"
            log(f"  [Warning] R2 thumbnail upload failed, using fallback URL: {r2_thumb_url}")

        if orig_upload_success:
            r2_orig_url = f"https://sovi-static-files.mysovi.ai/{r2_orig_key}"
        else:
            r2_orig_url = r2_thumb_url

        # Form the English final metadata JSON
        en_meta = {
            "character": en_name,
            "lang": "en",
            "universe": clean_text(en_data.get("universe", "Unknown")),
            "funFact": clean_text(en_data.get("funFact", "A mysterious entity.")),
            "imagePrompt": en_prompt,
            "imageUrl": r2_thumb_url  # Web client uses the compressed thumbnail!
        }

        # Form the Chinese final metadata JSON
        zh_meta = {
            "character": zh_name,
            "lang": "zh",
            "universe": clean_text(zh_data.get("universe", "未知")),
            "funFact": clean_text(zh_data.get("funFact", "一个神秘的角色。")),
            "imagePrompt": character_art_prompt(zh_name, zh_data.get("imagePrompt")),
            "imageUrl": r2_thumb_url  # Web client uses the compressed thumbnail!
        }

        # Upload both metadata JSON files to Cloudflare KV
        log(f"  Uploading English Metadata to Cloudflare KV (tcg_meta_{en_hash})...")
        write_to_kv(f"tcg_meta_{en_hash}", {**en_meta, "status": "done"}, logger=log)

        log(f"  Uploading Chinese Metadata to Cloudflare KV (tcg_meta_{zh_hash})...")
        write_to_kv(f"tcg_meta_{zh_hash}", {**zh_meta, "status": "done"}, logger=log)

        # Save progress locally
        csv_row = [
            category,
            en_name,
            zh_name,
            en_hash,
            zh_hash,
            r2_thumb_url,  # Web Client URL
            en_meta["universe"],
            en_meta["funFact"],
            zh_meta["universe"],
            zh_meta["funFact"]
        ]
        # Inject original image URL to CSV for reference as well
        csv_row.append(r2_orig_url)
        save_progress(en_hash, en_meta, zh_hash, zh_meta, csv_row)

        log(f"  [Success] {en_name} / {zh_name} fully pre-generated!")

        # Print the accumulated log block under thread-safe file_lock
        with file_lock:
            print("\\n".join(local_logs))

        return "generated"

    except Exception as e:
        log(f"  [Error] Failed to process {en_name} / {zh_name}: {e}")
        # Print logs under file_lock on error as well
        with file_lock:
            print("\\n".join(local_logs))
        raise e

"""

# Apply modifications
if old_upload_to_r2 in code:
    code = code.replace(old_upload_to_r2, new_upload_to_r2)
    print("✓ Replaced upload_to_r2")
else:
    print("⚠ Could not match old_upload_to_r2 exactly, doing a robust substring check...")
    # fallback
    code = code.replace("def upload_to_r2(local_path, r2_key):", "def upload_to_r2(local_path, r2_key, logger=None):")

if old_write_to_kv in code:
    code = code.replace(old_write_to_kv, new_write_to_kv)
    print("✓ Replaced write_to_kv")
else:
    print("⚠ Could not match old_write_to_kv exactly, doing fallback...")
    code = code.replace("def write_to_kv(key, json_val):", "def write_to_kv(key, json_val, logger=None):")

if old_compress_image in code:
    code = code.replace(old_compress_image, new_compress_image)
    print("✓ Replaced compress_image")
else:
    print("⚠ Could not match old_compress_image exactly, doing fallback...")
    code = code.replace("def compress_image(input_path, output_path, max_size_kb=300):", "def compress_image(input_path, output_path, max_size_kb=300, logger=None):")

# Swap process_character_row block
code = code[:idx_start] + new_process_block + code[idx_end:]
print("✓ Swapped process_character_row block")

# Save file back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Modification complete!")
