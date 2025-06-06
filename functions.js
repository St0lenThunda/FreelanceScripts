// functions.js - JS for FreelanceScripts landing page

// --- Zero Config Dynamic Tool Info Fetcher with .excluded filtering ---
// This function gets all tool folders, filters out those with a .excluded file, and fetches README info.
export async function getToolFolders () {
  let folders = [];
  try {
    // debugger
  
    const input = document.createElement( 'input' );
    input.type = 'file';
    input.style.display = 'none';
    document.body.appendChild( input );
    input.click();
    input.addEventListener( 'change', () => {
      console.log( 'Selected file:', input.files[0] );
      document.body.removeChild( input );
    } );
  if (!folders.length) throw new Error("Zero-Config Solution Pending");

  } catch ( e ) {
    folders = [
      'csv_json_converter',
      'scraper',
      'executioner',
      'package_toolkit',
      'readme_updater',
      'watch_automation',
      'toolkit_runner'
    ];
    console.info( `Error fetching folders: ${e}` )
    console.info(`Defaulting to ${ folders.length } tools`);
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

  // Dynamically create style map
  const colors = ['blue', 'green', 'purple', 'yellow', 'pink', 'cyan', 'red', 'orange'];
  const styleMap = filteredFolders.reduce( ( map, folder, index ) => {
    const color = colors[index % colors.length];
    map[folder] = {
      gradient: `from-${color}-900 via-gray-800 to-gray-900`,
      border: `border-${color}-700`,
      shadow: `hover:shadow-${color}-500/40`,
      text: `text-${color}-300`,
      btn: `bg-${color}-700 hover:bg-${color}-600`
    };
    return map;
  }, {} );

  // Helper to fetch README content and parse info
  async function fetchToolInfo ( folder ) {
    try {
      const resp = await fetch( `./${folder}/README.md` );
      if ( !resp.ok ) return null;
      const md = await resp.text();

      // Parse first heading as name (e.g., "# Tool Name")
      const nameMatch = md.match( /^#\s+(.+)/m );
      let name = nameMatch ? nameMatch[1].trim() : folder;
      console.log( 'Tool found:', name )
      // Extract emojis from the beginning of the name for use as a background
      const emojiMatch = name.split( ' ' )[0];
      const emojiBackground = emojiMatch;

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
    // Strip all leading '>' and whitespace from each line in the blockquote content
    const blockquoteContent = blockquoteMatch[1]
      .split( '\n' )
      .map( line => line.replace( /^\s*>?\s?/, '' ) )
      .join( '\n' )
      .trim();

    // Split lines and separate purpose and features based on "Key Features"
    const lines = blockquoteContent.split( '\n' );
    let purposeLines = [];
    let featuresLines = [];
    let foundKeyFeatures = false;
    for ( const line of lines ) {
      if ( !foundKeyFeatures && line.trim().toLowerCase().startsWith( 'key features' ) ) {
        foundKeyFeatures = true;
        continue; // skip the "Key Features" line itself
      }
      if ( !foundKeyFeatures ) {
        purposeLines.push( line );
      } else {
        featuresLines.push( line );
      }
    }

    // Remove empty lines and trim
    const descriptionLines = purposeLines.map( line => line.trim() ).filter( line => line !== '' );
    const featuresList = featuresLines.map( line => line.trim() ).filter( line => line !== '' );

    purpose = descriptionLines.join( '\n' );
    features = mdToHtml( featuresList.join( '\n' ) );
  }

  return { purpose, features };
}

// --- Dynamic Tool Card Rendering ---
// Returns HTML for a dynamically generated card based on the provided template
export function generateDynamicCard ( tool, idx, totalTools ) {
  const angle = [4, -8, -7, 11, 13, -17, 20][idx % 7];
  const prevIdx = ( idx - 1 + totalTools ) % totalTools + 1;
  const nextIdx = ( idx + 1 ) % totalTools + 1;
  const { purpose, features } = extractPurposeAndFeatures( tool.markdown || '' );
  const divider = `<div class='flex items-center'>
    <hr class='flex-grow border-gray-600'>
    <span class='mx-4 text-gray-400'>✦</span>
    <hr class='flex-grow border-gray-600'>
  </div>`;
  const iconAnimations = ['animate__bounce', 'animate__pulse', 'animate__rubberBand', 'animate__shakeX', 'animate__shakeY'];
  const randomIconAnimation = iconAnimations[Math.floor( Math.random() * iconAnimations.length )];

  // Wrap dynamic details in a scrollable area
  return `
  <input type="radio" id="radio-${idx + 1}" name="radio-card" ${idx === 0 ? 'checked' : ''}>
  <article class="card" style="--angle:${angle}deg">
      <div class="card-icon card-img bg-gradient-to-br ${tool.gradient} ${tool.text} ${tool.border} ${tool.shadow} flex items-center justify-center text-white border-8  p-4 bg-gray-800 ${randomIconAnimation}" style="width: 200px; height: 200px; font-size: 6rem;">
        <span>${tool.emojiBackground || '🔧'}</span>
      </div>
      <div class="card-data bg-gradient-to-br ${tool.gradient} ${tool.border} ${tool.shadow} rounded-lg p-4 shadow-md" style="height: 75vh">
      <span class="card-num ${tool.text} animate__animated animate__slideInLeft">${idx + 1}/${totalTools}</span>
      <h2 class="${tool.text} animate__animated animate__slideInDown text-3xl text-bold">${tool.name}</h2>
        <p class="${tool.text} animate__animated animate__slideInUp">
          <hr />
          ${purpose} 
          ${divider}
        </p>
        <div class="scrollable-details" style="height: 30px; overflow: hidden;">
          <details class="card-features detailsElement">
          <summary class='font-semibold text-lg mb-1 ${tool.text} animate__animated animate__slideInDown'>Key Features</summary>
          <ul class='list-disc ml-5 text-sm mt-2 ${tool.text} animate__animated animate__slideInLeft'>${features}</ul>
          </details>
        </div>
        <a href="${tool.readme}" class="card-btn ${tool.btn} rounded-full px-4 py-2 text-white font-semibold shadow-lg transition-transform duration-300 hover:scale-105 animate__animated animate__slideInUp" style="margin: 0 auto; display: block; width: fit-content;">Read More</a>
        <footer style="display: flex; justify-content: space-between; padding: 0 1rem;">
          <label for="radio-${prevIdx}" aria-label="Previous" class="${tool.text} animate__animated animate__slideInLeft">&#10094;</label>
          <label for="radio-${nextIdx}" aria-label="Next" class="${tool.text} animate__animated animate__slideInRight">&#10095;</label>
        </footer>
      </div>
    </article>
  `;
}

function addDetailsListeners () {
  
  // Listen for state toggling of the <details> element
  const detailsEls = document.querySelectorAll( ".detailsElement" )
  detailsEls.forEach( el => {    
    el.addEventListener( "toggle", function ( event ) {
      const modal = document.getElementById( "modal" );
      const modalContent = document.getElementById( "modalContent" );
      const backdrop = document.getElementById( "backdrop" );
    
      // If 'open' is true, copy inner content into the modal and display
      if ( event.target.open ) {
        modalContent.innerHTML = event.target.innerHTML;
        modal.classList.add( "show" );
        backdrop.classList.add( "show" );
        addCloseListener()
      } else {
        closeModal();
      }
    })
  } );
  
}

// Function to close the modal and remove backdrop
export const closeModal = () => {
  const modal = document.getElementById( "modal" );
  const backdrop = document.getElementById( "backdrop" );
  modal.classList.remove( "show" );
  backdrop.classList.remove( "show" );
}
export const addCloseListener = () => {
  const closeBtn = document.getElementById( 'closeButton' );
  const backdrop = document.getElementById( 'backdrop' );

  if ( closeBtn ) {
    closeBtn.addEventListener( 'click', closeModal );
  } else {
    console.warn( "Close button not found!" );
  }

  if ( backdrop ) {
    backdrop.addEventListener( 'click', closeModal );
  } else {
    console.warn( "Backdrop not found!" );
  }
}
// --- Carousel Rendering ---
// Renders the carousel with all tool cards
export async function renderCarousel () {
  console.log( "Generating tool list" )
  const cardsContainer = document.querySelector( '.cards' );
  if ( !cardsContainer ) return;
  const loading = ` <img
        src="./loading.webp"
        alt="Loading"
        class="mx-auto mb-4 animate__animated animate__pulse animate__infinite"
        style="width=150px; height: 150px;"
      >`
  cardsContainer.innerHTML = loading
  setTimeout( async () => {
    const tools = await getToolFolders();
    
    // Render dynamic cards
    cardsContainer.innerHTML = tools.map( ( tool, idx ) => generateDynamicCard( tool, idx, tools.length ) ).join( '' );

    addDetailsListeners()
  }, 3000 );
}
