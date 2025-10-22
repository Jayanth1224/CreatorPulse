export interface NewsletterSection {
  id: string;
  type: 'intro' | 'insights' | 'trends' | 'conclusion' | 'custom';
  title: string;
  content: string;
  order: number;
}

export function parseNewsletterSections(htmlContent: string): NewsletterSection[] {
  const sections: NewsletterSection[] = [];
  let order = 0;

  // Create a temporary DOM element to parse the HTML
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlContent, 'text/html');
  
  // Find all heading elements (h1, h2, h3) and their following content
  const headings = doc.querySelectorAll('h1, h2, h3');
  
  if (headings.length === 0) {
    // If no headings found, treat entire content as intro
    return [{
      id: 'intro-1',
      type: 'intro',
      title: 'Introduction',
      content: htmlContent,
      order: 0
    }];
  }

  headings.forEach((heading, index) => {
    const headingText = heading.textContent?.trim() || '';
    const headingLevel = parseInt(heading.tagName.charAt(1));
    
    // Determine section type based on heading text
    let sectionType: NewsletterSection['type'] = 'custom';
    if (headingText.toLowerCase().includes('insight')) {
      sectionType = 'insights';
    } else if (headingText.toLowerCase().includes('trend')) {
      sectionType = 'trends';
    } else if (headingText.toLowerCase().includes('conclusion') || headingText.toLowerCase().includes('summary')) {
      sectionType = 'conclusion';
    } else if (index === 0) {
      sectionType = 'intro';
    }

    // Get content following this heading until the next heading
    let content = '';
    let nextElement = heading.nextElementSibling;
    
    while (nextElement && !['H1', 'H2', 'H3'].includes(nextElement.tagName)) {
      content += nextElement.outerHTML;
      nextElement = nextElement.nextElementSibling;
    }

    // If no content found, try to get text content
    if (!content.trim()) {
      content = heading.parentElement?.innerHTML || '';
    }

    sections.push({
      id: `${sectionType}-${index + 1}`,
      type: sectionType,
      title: headingText || `${sectionType.charAt(0).toUpperCase() + sectionType.slice(1)} ${index + 1}`,
      content: content.trim() || heading.outerHTML,
      order: order++
    });
  });

  return sections;
}

export function reassembleNewsletterSections(sections: NewsletterSection[]): string {
  return sections
    .sort((a, b) => a.order - b.order)
    .map(section => {
      if (section.type === 'intro' && !section.title.toLowerCase().includes('intro')) {
        return section.content;
      }
      return `<h2>${section.title}</h2>\n${section.content}`;
    })
    .join('\n\n');
}

export function getSectionIcon(type: NewsletterSection['type']): string {
  switch (type) {
    case 'intro':
      return '📝';
    case 'insights':
      return '💡';
    case 'trends':
      return '📈';
    case 'conclusion':
      return '🎯';
    default:
      return '📄';
  }
}
