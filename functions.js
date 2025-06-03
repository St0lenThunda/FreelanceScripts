// functions.js - JS for FreelanceScripts landing page

// --- Zero Config Dynamic Tool Info Fetcher with .excluded filtering ---
// This function gets all tool folders, filters out those with a .excluded file, and fetches README info.
export async function getToolFolders () {
  let folders = [];
  try {
    // Static fallback for local dev/live server (directory listing fetch is unreliable)
    folders = [
      'csv_json_converter',
      'scraper',
      'executioner',
      'package_toolkit',
      'readme_updater',
      'watch_automation'
    ];
  } catch ( e ) {
    folders = [
      'csv_json_converter',
      'scraper',
      'executioner',
      'package_toolkit',
      'readme_updater',
      'watch_automation'
    ];
  }
  // Filter out folders with a .excluded file
  const filteredFolders = [];
  for ( const folder of folders ) {
    try {
      const excl = await fetch( `${folder}/.excluded`, { method: 'HEAD' } );
      if ( excl.ok ) continue;
    } catch ( e ) { }
    filteredFolders.push( folder );
  }
  // Styling map by folder name
  const styleMap = {
    csv_json_converter: {
      gradient: 'from-blue-900 via-gray-800 to-gray-900', border: 'border-blue-700', shadow: 'hover:shadow-blue-500/40', text: 'text-blue-300', btn: 'bg-blue-700 hover:bg-blue-600'
    },
    scraper: {
      gradient: 'from-green-900 via-gray-800 to-gray-900', border: 'border-green-700', shadow: 'hover:shadow-green-500/40', text: 'text-green-300', btn: 'bg-green-700 hover:bg-green-600'
    },
    executioner: {
      gradient: 'from-purple-900 via-gray-800 to-gray-900', border: 'border-purple-700', shadow: 'hover:shadow-purple-500/40', text: 'text-purple-300', btn: 'bg-purple-700 hover:bg-purple-600'
    },
    package_toolkit: {
      gradient: 'from-yellow-900 via-gray-800 to-gray-900', border: 'border-yellow-700', shadow: 'hover:shadow-yellow-500/40', text: 'text-yellow-200', btn: 'bg-yellow-700 hover:bg-yellow-600'
    },
    readme_updater: {
      gradient: 'from-pink-900 via-gray-800 to-gray-900', border: 'border-pink-700', shadow: 'hover:shadow-pink-500/40', text: 'text-pink-200', btn: 'bg-pink-700 hover:bg-pink-600'
    },
    watch_automation: {
      gradient: 'from-cyan-900 via-gray-800 to-gray-900', border: 'border-cyan-700', shadow: 'hover:shadow-cyan-500/40', text: 'text-cyan-200', btn: 'bg-cyan-700 hover:bg-cyan-600'
    }
  };

  // Helper to fetch README content and parse info
  async function fetchToolInfo ( folder ) {
    try {
      const resp = await fetch( `./${folder}/README.md` );
      if ( !resp.ok ) return null;
      const md = await resp.text();

      // Parse first heading as name (e.g., "# Tool Name")
      const nameMatch = md.match( /^#\s+(.+)/m );
      let name = nameMatch ? nameMatch[1].trim() : folder;
      console.log( 'Name', name )
      // Extract emojis from the beginning of the name for use as a background
      const emojiMatch = name.split( ' ' )[0];
      const emojiBackground = emojiMatch;

      // // Remove emojis from the name
      // if ( emojiBackground ) {
      //   name = name.replace( emojiBackground, '' ).trim();
      // }

      // Parse blockquote entitled Purpose as description (e.g., "> Purpose\nDescription text")
      const descMatch = md.match( /^>\s*Purpose[\s\n]+([\s\S]*?)(?=\n>\s*$)/i );

      // Extract Key Features section immediately after Purpose (e.g., "> Key Features\n- Feature 1\n- Feature 2")
      const featuresMatch = md.match( /(?<=\n>\s*$)[\s\S]*?(?=\n#|\n##|$)/i );

      // Convert Purpose and Features to HTML
      const purposeHtml = descMatch ? `<h4 class='font-semibold text-lg mt-2 mb-1'>Purpose</h4>${mdToHtml( descMatch[1].trim() )}` : '';
      const featuresHtml = featuresMatch ? `<h4 class='font-semibold text-lg mt-2 mb-1'>Key Features</h4>${mdToHtml( featuresMatch[0].trim() )}` : '';

      return {
        folder,
        name, // Name without emojis
        desc: descMatch ? descMatch[1].trim() : '', // Use the blockquote entitled Purpose as the description
        features: featuresMatch ? featuresMatch[0].trim().split( /\n\- / ).slice( 1 ) : [], // Extracted features as an array
        purposeHtml, // HTML-ready Purpose section
        featuresHtml, // HTML-ready Features section
        emojiBackground, // Extracted emojis for background
        readme: `./${folder}/README.md`,
        markdown: md // Full markdown content for further processing
      };
    } catch ( e ) {
      return null;
    }
  }
  // Gather all tool info
  const toolInfo = ( await Promise.all( filteredFolders.map( fetchToolInfo ) ) ).filter( Boolean );
  // Assign styling
  toolInfo.forEach( tool => Object.assign( tool, styleMap[tool.folder] || {} ) );
  return toolInfo;
}

// --- Markdown to HTML Conversion ---
// Converts markdown to HTML with TailwindCSS classes
export function mdToHtml ( md ) {
  md = md.replace( /^# (.*$)/gim, '<h2 class="text-xl font-bold mb-2">$1</h2>' ); // Convert top-level # headings to h2
  md = md.replace( /\*\*(.*?)\*\*/gim, '<b>$1</b>' ); // Convert **bold** to <b>
  md = md.replace( /\*(.*?)\*/gim, '<i>$1</i>' ); // Convert *italic* to <i>
  md = md.replace( /\[(.*?)\]\((.*?)\)/gim, '<a href="$2" class="text-blue-400 underline">$1</a>' ); // Convert [text](url) to <a href="url">text</a>
  md = md.replace( /^\s*\- (.*)$/gim, '<li>$1</li>' ); // Convert lines starting with - (markdown list) to <li>
  md = md.replace( /(<li>.*<\/li>)/gims, '<ul class="list-disc ml-5 text-sm mb-4">$1</ul>' ); // Wrap consecutive <li> elements in a <ul>
  md = md.replace( /^(?!<h2|<ul|<li|<b|<i|<a)([^\n]+)\n/gm, '<p class="mb-2">$1</p>' ); // Convert any line not already wrapped in a tag to a <p>
  return md;
}

// --- Extract Purpose and Key Features from Markdown ---
// Returns { purpose, features } with markdown converted to HTML
export function extractPurposeAndFeatures ( md ) {
  let purpose = '';
  let features = '';

  // Extract Purpose section starting with '> ## Purpose'
  const blockquoteMatch = md.match( />\s*##\s*Purpose[\s\n]+([\s\S]*?)(?=\n[^>]|$)/i );
  if ( blockquoteMatch ) {
    const blockquoteContent = blockquoteMatch[1].trim();
    const lines = blockquoteContent.split( /\n>/ ).map( line => line.trim() );

    // Separate description and features
    const descriptionEndIndex = lines.findIndex( line => line === '> ' );
    const descriptionLines = lines.slice( 0, descriptionEndIndex );
    const featuresLines = lines.slice( descriptionEndIndex + 1 );

    purpose = mdToHtml( descriptionLines.join( '\n' ) );
    features = mdToHtml( featuresLines.join( '\n' ) );
  }

  return { purpose, features };
}

// --- Tool Card Rendering ---
// Returns HTML for a tool card given tool info and index
export function createToolCard ( tool, idx ) {
  // Animation classes for carousel entry effects
  const anims = [
    'animate__slideInLeft',
    'animate__slideInUp',
    'animate__slideInRight',
    'animate__slideInDown',
    'animate__slideInLeft',
    'animate__slideInRight'
  ];
  // Extract the 'Purpose' and 'Key Features' sections from the tool's README markdown
  const { purpose, features } = extractPurposeAndFeatures( tool.markdown || '' );
  console.log( 'Purpose:', purpose );
  console.log( 'Features:', features );
  // We'll build up the HTML for the details section here
  let detailsHtml = '';
  // If a Purpose section was found, add it as a heading and paragraph
  if ( purpose ) {
    detailsHtml += `<h4 class='font-semibold text-lg mt-2 mb-1'>Purpose</h4>`;
    detailsHtml += `<p class='mb-2 text-gray-200'>${purpose.replace( /\n/g, '<br>' )}</p>`;
  }
  detailsHtml += `\n        <div class='my-4 flex items-center'>\n          <hr class='flex-grow border-gray-600'>\n          <span class='mx-4 text-gray-400'>✦</span>\n          <hr class='flex-grow border-gray-600'>\n        </div>\n      `;
  // If Key Features were found, add a stylized divider and then the features list in <details>
  if ( features && features.length ) {
    detailsHtml += `<details class='mb-4'><summary class='font-semibold text-lg cursor-pointer'>Features</summary><ul class='list-disc ml-5 text-sm mt-2'>${features.map( f => `<li>${f.replace( /^\-\s+/, '' )}</li>` ).join( '' )}</ul></details>`;
  }
  // Return the full HTML for the tool card
  return `\n    <div class="carousel-item tool-card bg-gradient-to-br ${tool.gradient} rounded-2xl p-8 shadow-2xl border ${tool.border} animate__animated ${anims[idx % anims.length]} animate__faster transition-transform duration-300 hover:scale-105 ${tool.shadow}">\n      <h3 class="text-2xl font-bold mb-2 ${tool.text} animate__animated animate__fadeInDown">${tool.name}</h3>\n      ${detailsHtml}\n      <a href="${tool.readme}" class="inline-block mb-2 px-4 py-2 ${tool.btn} rounded-full text-white font-semibold shadow transition animate__animated animate__fadeInUp animate__delay-3s">Read more</a>\n    </div>\n  `;
}

// --- Carousel Rendering ---
// Renders the carousel with all tool cards
export async function renderCarousel () {
  const carousel = document.querySelector( '.carousel' );
  if ( !carousel ) return;
  const tools = await getToolFolders();
  console.log( 'DEBUG: tools array for carousel:', tools );
  carousel.innerHTML = tools.map( createToolCard ).join( '' );
}

// --- Carousel Navigation ---
// Adds left/right scroll logic to carousel arrows
export function setupCarouselNav () {
  const carousel = document.querySelector( '.carousel' );
  document.getElementById( 'carousel-left' ).onclick = () => carousel.scrollBy( { left: -carousel.offsetWidth * 0.8, behavior: 'smooth' } );
  document.getElementById( 'carousel-right' ).onclick = () => carousel.scrollBy( { left: carousel.offsetWidth * 0.8, behavior: 'smooth' } );
}
