(() => {
  const button = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.site-nav');
  if (button && nav) {
    button.addEventListener('click', () => {
      const isOpen = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!isOpen));
      nav.classList.toggle('is-open', !isOpen);
    });
  }

  const article = document.querySelector('[data-article-body]');
  const toc = document.querySelector('[data-toc]');
  const tocList = document.querySelector('[data-toc-list]');
  if (article && toc && tocList) {
    const headings = [...article.querySelectorAll('h2, h3')];
    if (headings.length >= 2) {
      const list = document.createElement('ol');
      headings.forEach((heading, index) => {
        if (!heading.id) heading.id = `section-${index + 1}`;
        const item = document.createElement('li');
        if (heading.tagName === 'H3') item.className = 'toc-subitem';
        const link = document.createElement('a');
        link.href = `#${heading.id}`;
        link.textContent = heading.textContent;
        item.appendChild(link);
        list.appendChild(item);
      });
      tocList.appendChild(list);
      toc.hidden = false;
    }
  }

  document.querySelectorAll('pre').forEach((block) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'code-block';
    block.parentNode.insertBefore(wrapper, block);
    wrapper.appendChild(block);
    const copy = document.createElement('button');
    copy.type = 'button';
    copy.className = 'copy-code';
    copy.textContent = 'Copy';
    copy.setAttribute('aria-label', 'Copy code');
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(block.innerText);
        copy.textContent = 'Copied';
        setTimeout(() => { copy.textContent = 'Copy'; }, 1600);
      } catch (_) {
        copy.textContent = 'Copy failed';
      }
    });
    wrapper.appendChild(copy);
  });
})();
