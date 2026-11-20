# Building VideoTransformer.exe (graphical guide)

**Status: the build has never been run.** Treat the result as unverified until you finish step 6.
You only need this if you want a copy that runs without the `tools` download step. The `.bat` launcher already
works without building anything.

## Option A: build on your own PC (no terminal)

1. Extract the project (see `README-WINDOWS.md`) to e.g. `C:\VideoTransformer`. You need internet and about 3 GB free.
2. Double-click **build_exe.bat**. (SmartScreen: **More info**, then **Run anyway**.)
3. Wait 5 to 15 minutes. It downloads uv, a private Python 3.12, ffmpeg and PyInstaller, then builds.
   Your Python 3.15.2 is not used (PyInstaller and Gradio may not support it).
4. When it says "Build finished", open the `dist\VideoTransformer` folder in File Explorer.
5. The program is `VideoTransformer.exe`. Keep the whole `VideoTransformer` folder together, because it is not a
   single file. You can right-click `VideoTransformer.exe`, then **Send to**, then **Desktop (create shortcut)**.
6. **Test before trusting it.**
   1. Double-click `VideoTransformer.exe`. A black window opens and then your browser opens the app.
   2. Color tab: upload a short video, apply "Cinematic", confirm the result plays and download works.
   3. Voice tab: use a video with sound, apply "Deep", confirm the sound changed and stays in sync.
   4. Object tab: confirm it says "Not available" (unless you connected a service), and Settings tab opens.
   5. Close the black window and confirm the app stops.
   6. Test on a second Windows PC that has no Python, to be sure nothing relies on your machine.

## Option B: build in the cloud with GitHub (no install on your PC)

1. Create a free GitHub account and a new **private** repository. Click **Add file**, then **Upload files**, drag the whole
   project folder contents in (keep the `.github` folder), and click **Commit changes**.
2. Open the **Actions** tab. If asked, click **I understand my workflows, go ahead and enable them**.
3. Choose **Build Windows executable** on the left, then **Run workflow**, then the green **Run workflow** button.
4. Wait about 10 to 20 minutes for a green check. The workflow runs the tests, builds the exe, and runs
   `VideoTransformer.exe --selftest` (a green check means that smoke test passed; it does **not** replace step 6 above).
5. Click the finished run, scroll to **Artifacts**, download **VideoTransformer-windows**, unzip it, and do step 6 above.

## If the build fails

- Scroll to the **first** error message in the black window (later ones are usually consequences).
- Common causes: no internet or blocked GitHub downloads (try without VPN, allow `github.com`), antivirus quarantining
  files in `tools\` (add an exception for the project folder), low disk space.
- Gradio is the most likely trouble spot. Its dynamically loaded parts are listed in `video-transformer.spec`; a
  message like `ModuleNotFoundError: No module named 'xyz'` when running the exe means `xyz` must be added to
  `hiddenimports` in that file.
- Send me the black window text and `%LOCALAPPDATA%\VideoTransformer\logs\app.log`.

## Known limits of the exe

- Folder build, not a single file. Antivirus tools sometimes flag unsigned PyInstaller programs; that is a
  false positive risk of unsigned software, not proof of a problem.
- It keeps the black console window as its status window; closing it quits the app.
- Object & Character mode still needs your own AI service (Settings tab).
