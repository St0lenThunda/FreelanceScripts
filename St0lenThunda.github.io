<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="UTF-8">
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0"
    >
    <title>FreelanceScripts - Python Starter Toolkit</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Animate.css CDN -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
    />
    <link
      rel="icon"
      type="image/png"
      href="../PythonStarter.png"
    >
    <style>
      .tool-card:hover {
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
      }

      .carousel {
        scroll-snap-type: x mandatory;
        overflow-x: auto;
        display: flex;
      }

      .carousel-item {
        scroll-snap-align: start;
        flex: 0 0 90%;
        margin-right: 2rem;
      }
    </style>
  </head>

  <body class="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700 min-h-screen text-gray-100">
    <header class="py-8 text-center animate__animated animate__fadeInDown">
      <img
        src="../PythonStarter.png"
        alt="FreelanceScripts Logo"
        class="mx-auto w-24 mb-4 animate__animated animate__pulse animate__infinite"
      >
      <h1 class="text-4xl md:text-5xl font-extrabold mb-2">FreelanceScripts</h1>
      <p class="text-xl md:text-2xl font-light mb-4">Python Starter Toolkit for Freelancers, Debuggers, and Builders</p>
      <div class="flex justify-center gap-4 mb-2">
        <span class="bg-blue-700 px-3 py-1 rounded-full text-sm">MIT License</span>
        <span class="bg-green-700 px-3 py-1 rounded-full text-sm">Python 3.8+</span>
        <span class="bg-purple-700 px-3 py-1 rounded-full text-sm">Linux | Mac | WSL</span>
      </div>
      <p class="mt-2 text-gray-400">Battle-tested, modular, and educational Python tools for your freelance journey.</p>
    </header>

    <main class="max-w-5xl mx-auto px-4">
      <!-- Tool Carousel -->
      <section class="my-12">
        <h2 class="text-3xl font-bold mb-6 text-center animate__animated animate__fadeIn">Included Tools</h2>
        <div class="relative">
          <div class="carousel pb-4 gap-8 px-2 md:px-8">
            <!-- Tool Cards Start -->
            <div
              class="carousel-item tool-card bg-gradient-to-br from-blue-900 via-gray-800 to-gray-900 rounded-2xl p-8 shadow-2xl border border-blue-700 animate__animated animate__slideInLeft animate__faster transition-transform duration-300 hover:scale-105 hover:shadow-blue-500/40"
            >
              <h3 class="text-2xl font-bold mb-2 text-blue-300 animate__animated animate__fadeInDown">CSV ⇄ JSON
                Converter</h3>
              <div class="mb-2 text-gray-300 animate__animated animate__fadeInLeft animate__delay-1s">A two-way data
                converter for CSV and JSON files.</div>
              <ul class="list-disc ml-5 text-sm mb-4 animate__animated animate__fadeInUp animate__delay-2s">
                <li>Converts CSV to JSON and JSON to CSV</li>
                <li>Interactive prompts and file listing</li>
                <li>Auto-naming and output inference</li>
                <li>Educational: heavily commented code</li>
              </ul>
              <a
                href="../csv_json_converter/README.md"
                class="inline-block mt-2 px-4 py-2 bg-blue-700 rounded-full text-white font-semibold shadow hover:bg-blue-600 transition animate__animated animate__fadeInUp animate__delay-3s"
              >Read more</a>
            </div>
            <div
              class="carousel-item tool-card bg-gradient-to-br from-green-900 via-gray-800 to-gray-900 rounded-2xl p-8 shadow-2xl border border-green-700 animate__animated animate__slideInUp animate__faster transition-transform duration-300 hover:scale-105 hover:shadow-green-500/40"
            >
              <h3 class="text-2xl font-bold mb-2 text-green-300 animate__animated animate__fadeInDown">Simple Web
                Scraper</h3>
              <div class="mb-2 text-gray-300 animate__animated animate__fadeInLeft animate__delay-1s">A modular web
                scraper that fetches titles and links from URLs.</div>
              <ul class="list-disc ml-5 text-sm mb-4 animate__animated animate__fadeInUp animate__delay-2s">
                <li>Fetches and parses HTML with BeautifulSoup</li>
                <li>Selector suggestion and ranking</li>
                <li>Handles multiple URLs and output formats</li>
                <li>Educational: modular and commented</li>
              </ul>
              <a
                href="../scraper/README.md"
                class="inline-block mt-2 px-4 py-2 bg-green-700 rounded-full text-white font-semibold shadow hover:bg-green-600 transition animate__animated animate__fadeInUp animate__delay-3s"
              >Read more</a>
            </div>
            <div
              class="carousel-item tool-card bg-gradient-to-br from-purple-900 via-gray-800 to-gray-900 rounded-2xl p-8 shadow-2xl border border-purple-700 animate__animated animate__slideInRight animate__faster transition-transform duration-300 hover:scale-105 hover:shadow-purple-500/40"
            >
              <h3 class="text-2xl font-bold mb-2 text-purple-300 animate__animated animate__fadeInDown">Executioner</h3>
              <div class="mb-2 text-gray-300 animate__animated animate__fadeInLeft animate__delay-1s">Automates making
                Python scripts executable and symlinking them for easy PATH usage.</div>
              <ul class="list-disc ml-5 text-sm mb-4 animate__animated animate__fadeInUp animate__delay-2s">
                <li>Finds and symlinks *_tool.py scripts</li>
                <li>Normalizes line endings</li>
                <li>Exclusion by marker file</li>
                <li>Educational: clear, stepwise comments</li>
              </ul>
              <a
                href="../executioner/README.md"
                class="inline-block mt-2 px-4 py-2 bg-purple-700 rounded-full text-white font-semibold shadow hover:bg-purple-600 transition animate__animated animate__fadeInUp animate__delay-3s"
              >Read more</a>
            </div>
            <div
              class="carousel-item tool-card bg-gradient-to-br from-yellow-900 via-gray-800 to-gray-900 rounded-2xl p-8 shadow-2xl border border-yellow-700 animate__animated animate__slideInDown animate__faster transition-transform duration-300 hover:scale-105 hover:shadow-yellow-500/40"
            >
              <h3 class="text-2xl font-bold mb-2 text-yellow-200 animate__animated animate__fadeInDown">Package Toolkit
              </h3>
              <div class="mb-2 text-gray-300 animate__animated animate__fadeInLeft animate__delay-1s">Packages all tools
                into a zip archive, generates a combined README, and respects exclusion rules.</div>
              <ul class="list-disc ml-5 text-sm mb-4 animate__animated animate__fadeInUp animate__delay-2s">
                <li>Recursively scans and packages tools</li>
                <li>Exclusion logic and marker files</li>
                <li>Dynamic combined README generation</li>
                <li>Educational: robust and safe</li>
              </ul>
              <a
                href="../package_toolkit/README.md"
                class="inline-block mt-2 px-4 py-2 bg-yellow-700 rounded-full text-white font-semibold shadow hover:bg-yellow-600 transition animate__animated animate__fadeInUp animate__delay-3s"
              >Read more</a>
            </div>
            <div
              class="carousel-item tool-card bg-gradient-to-br from-pink-900 via-gray-800 to-gray-900 rounded-2xl p-8 shadow-2xl border border-pink-700 animate__animated animate__slideInLeft animate__faster transition-transform duration-300 hover:scale-105 hover:shadow-pink-500/40"
            >
              <h3 class="text-2xl font-bold mb-2 text-pink-200 animate__animated animate__fadeInDown">README Updater
              </h3>
              <div class="mb-2 text-gray-300 animate__animated animate__fadeInLeft animate__delay-1s">A modular
                framework for dynamically updating the main and tool READMEs.</div>
              <ul class="list-disc ml-5 text-sm mb-4 animate__animated animate__fadeInUp animate__delay-2s">
                <li>Modular task system for README management</li>
                <li>Syncs Purpose sections from docstrings</li>
                <li>Automates tool table updates</li>
                <li>Educational: extensible and clear</li>
              </ul>
              <a
                href="../readme_updater/README.md"
                class="inline-block mt-2 px-4 py-2 bg-pink-700 rounded-full text-white font-semibold shadow hover:bg-pink-600 transition animate__animated animate__fadeInUp animate__delay-3s"
              >Read more</a>
            </div>
            <div
              class="carousel-item tool-card bg-gradient-to-br from-cyan-900 via-gray-800 to-gray-900 rounded-2xl p-8 shadow-2xl border border-cyan-700 animate__animated animate__slideInRight animate__faster transition-transform duration-300 hover:scale-105 hover:shadow-cyan-500/40"
            >
              <h3 class="text-2xl font-bold mb-2 text-cyan-200 animate__animated animate__fadeInDown">Watch Automation
              </h3>
              <div class="mb-2 text-gray-300 animate__animated animate__fadeInLeft animate__delay-1s">Automatically
                updates the main README tool table when any tool's README changes.</div>
              <ul class="list-disc ml-5 text-sm mb-4 animate__animated animate__fadeInUp animate__delay-2s">
                <li>Monitors tool directories for README changes</li>
                <li>Runs updater automatically</li>
                <li>Logs all activity</li>
                <li>Educational: modular and extensible</li>
              </ul>
              <a
                href="../watch_automation/README.md"
                class="inline-block mt-2 px-4 py-2 bg-cyan-700 rounded-full text-white font-semibold shadow hover:bg-cyan-600 transition animate__animated animate__fadeInUp animate__delay-3s"
              >Read more</a>
            </div>
          </div>
          <div class="absolute left-0 top-1/2 -translate-y-1/2 z-10">
            <button
              id="carousel-left"
              class="bg-gray-700 bg-opacity-80 hover:bg-blue-700 text-white rounded-full p-2 shadow-lg focus:outline-none animate__animated animate__fadeInLeft"
            ><svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 19l-7-7 7-7"
                />
              </svg></button>
          </div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 z-10">
            <button
              id="carousel-right"
              class="bg-gray-700 bg-opacity-80 hover:bg-blue-700 text-white rounded-full p-2 shadow-lg focus:outline-none animate__animated animate__fadeInRight"
            ><svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg></button>
          </div>
        </div>
        <p class="text-center text-gray-400 mt-4">Scroll horizontally or use arrows to browse all tools &rarr;</p>
      </section>

      <!-- Concepts Section -->
      <section class="my-12 animate__animated animate__fadeInUp">
        <h2 class="text-3xl font-bold mb-4 text-center">Pythonic Concepts</h2>
        <div class="bg-gray-800 rounded-xl p-6 shadow-lg">
          <details open>
            <summary class="text-xl font-semibold cursor-pointer">Unique Pythonic Concepts in This Project</summary>
            <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <b>Argument parsing</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Handles command-line arguments and interactive prompts for flexible usage.</li>
                  <li>Uses <code>argparse</code> for flexible CLI usage.</li>
                </ul>
                <b>Command-line</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Handles CLI arguments for flexible script behavior.</li>
                </ul>
                <b>Csv and json handling</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Uses Python's built-in <code>csv</code> and <code>json</code> modules for data conversion.</li>
                </ul>
                <b>Docstring extraction and markdown conversion</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Extracts Python docstrings, preserves formatting, and safely converts HTML tags for markdown.</li>
                </ul>
                <b>Dynamic documentation</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Automates the generation of a combined README by reading and summarizing other README files.</li>
                  <li>Automates updates to README files based on project state.</li>
                </ul>
                <b>Educational comments</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Explains each step for learning purposes.</li>
                </ul>
                <b>Error handling</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Checks for file existence and handles missing/invalid files gracefully.</li>
                  <li>Provides robust error messages and suggestions.</li>
                </ul>
              </div>
              <div>
                <b>Exclusion by marker file</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Skips directories containing a <code>.excluded</code> file.</li>
                </ul>
                <b>Exclusion logic</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Shows how to exclude files/folders based on patterns and marker files (e.g.,
                    <code>.excluded</code>).
                  </li>
                </ul>
                <b>File and directory traversal</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Uses <code>pathlib.Path</code> and <code>rglob</code> to recursively walk directories and process
                    files.</li>
                </ul>
                <b>File I/O</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Reading and writing files using <code>open</code>, with context managers for safety.</li>
                </ul>
                <b>File listing</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Lists files by extension using <code>pathlib</code> and <code>glob</code>.</li>
                </ul>
                <b>File parsing</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Reads and updates Markdown files programmatically.</li>
                </ul>
                <b>Logging</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Logs activity to both terminal and file for auditing.</li>
                </ul>
                <b>Modular task system</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Uses classes and inheritance to enable extensible task management.</li>
                </ul>
                <b>Subprocess automation</b>
                <ul class="list-disc ml-5 text-sm">
                  <li>Runs other scripts automatically in response to file events.</li>
                </ul>
              </div>
            </div>
          </details>
        </div>
      </section>

      <!-- Project Structure Section -->
      <section class="my-12 animate__animated animate__fadeInUp">
        <h2 class="text-3xl font-bold mb-4 text-center">Project Structure</h2>
        <div class="bg-gray-800 rounded-xl p-6 shadow-lg overflow-x-auto">
          <pre class="text-sm text-gray-300 whitespace-pre">.
├── README.md
├── csv_json_converter/
│   ├── csv_to_json_converter_tool.py
│   ├── example.csv
│   ├── example.json
│   └── README.md
├── debug_demo/
│   ├── README.md
│   ├── scraper_bugfix_tool.py
│   └── scraper_buggy_tool.py
├── executioner/
│   ├── executioner_tool.py
│   └── README.md
├── package_toolkit/
│   ├── package_toolkit_tool.py
│   └── README.md
├── readme_updater/
│   ├── readme_updater_tool.py
│   └── README.md
├── scraper/
│   ├── README.md
│   └── simple_scraper_tool.py
├── watch_automation/
│   ├── README.md
│   ├── watch_automation_tool.py
│   └── watch_automation.log
</pre>
        </div>
      </section>
    </main>

    <footer class="py-8 text-center text-gray-500 animate__animated animate__fadeInUp">
      <p>&copy; 2025 StolenThunda &mdash; MIT License. <a
          href="https://github.com/St0lenThunda/FreelanceScripts"
          class="text-blue-400 underline"
        >GitHub Repo</a></p>
    </footer>

    <script type="module">
      import { renderCarousel, setupCarouselNav } from './functions.js';
      // Render the carousel on DOMContentLoaded
      document.addEventListener( 'DOMContentLoaded', () => {
        renderCarousel();
        setupCarouselNav();
      } );
    </script>
  </body>

</html>