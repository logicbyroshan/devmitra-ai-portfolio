// legal.js - JavaScript for Legal Pages (Privacy Policy & Terms of Service)

document.addEventListener('DOMContentLoaded', () => {
    // Exit early if this is not a legal page
    if (!document.body.classList.contains('legal-page')) {
        return;
    }

    // Animation system is now handled by animations.js
    // No need for duplicate animation code here

    // =========================================================================
    // SMOOTH SCROLL FOR INTERNAL LINKS
    // =========================================================================
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const headerOffset = 80; // Account for fixed header
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // =========================================================================
    // COPY LINK FUNCTIONALITY
    // =========================================================================
    const headings = document.querySelectorAll('.legal-section h2, .legal-section h3');
    headings.forEach((heading, index) => {
        // Add ID if not already present
        if (!heading.id) {
            heading.id = `section-${index + 1}`;
        }

        // Add click handler to copy link
        heading.addEventListener('click', () => {
            const url = `${window.location.origin}${window.location.pathname}#${heading.id}`;

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(url).then(() => {
                    showCopyNotification(heading);
                }).catch(() => {
                    fallbackCopyTextToClipboard(url, heading);
                });
            } else {
                fallbackCopyTextToClipboard(url, heading);
            }
        });

        // Add cursor pointer style
        heading.style.cursor = 'pointer';
        heading.title = 'Click to copy link to this section';
    });

    // =========================================================================
    // COPY NOTIFICATION
    // =========================================================================
    function showCopyNotification(element) {
        // Remove any existing notifications
        const existingNotifications = document.querySelectorAll('.copy-notification');
        existingNotifications.forEach(notification => notification.remove());

        // Create and show notification
        const notification = document.createElement('div');
        notification.className = 'copy-notification';
        notification.textContent = 'Link copied to clipboard!';
        notification.style.cssText = `
            position: absolute;
            background: var(--accent-color);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            z-index: 1000;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            pointer-events: none;
        `;

        // Position notification
        const rect = element.getBoundingClientRect();
        notification.style.left = `${rect.left}px`;
        notification.style.top = `${rect.top - 40}px`;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        }, 10);

        // Remove after delay
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-10px)';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    // =========================================================================
    // FALLBACK COPY FUNCTION
    // =========================================================================
    function fallbackCopyTextToClipboard(text, element) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showCopyNotification(element);
            }
        } catch (err) {
            console.error('Unable to copy link: ', err);
        }

        document.body.removeChild(textArea);
    }

    // =========================================================================
    // TABLE OF CONTENTS (IF IMPLEMENTED)
    // =========================================================================
    const tocButton = document.querySelector('.toc-toggle');
    const tocContainer = document.querySelector('.table-of-contents');

    if (tocButton && tocContainer) {
        tocButton.addEventListener('click', () => {
            tocContainer.classList.toggle('toc-visible');
            tocButton.classList.toggle('toc-active');
        });

        // Close TOC when clicking outside
        document.addEventListener('click', (e) => {
            if (!tocContainer.contains(e.target) && !tocButton.contains(e.target)) {
                tocContainer.classList.remove('toc-visible');
                tocButton.classList.remove('toc-active');
            }
        });
    }

    // =========================================================================
    // BACK TO TOP BUTTON
    // =========================================================================
    const backToTopButton = document.createElement('button');
    backToTopButton.className = 'back-to-top';
    backToTopButton.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--accent-color);
        color: white;
        border: none;
        cursor: pointer;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    `;

    document.body.appendChild(backToTopButton);

    // Show/hide back to top button
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.opacity = '1';
            backToTopButton.style.transform = 'translateY(0)';
        } else {
            backToTopButton.style.opacity = '0';
            backToTopButton.style.transform = 'translateY(20px)';
        }
    });

    // Back to top click handler
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // =========================================================================
    // ENHANCED ACCESSIBILITY
    // =========================================================================

    // Add skip links for better navigation
    const skipLinks = document.createElement('div');
    skipLinks.className = 'skip-links';
    skipLinks.innerHTML = `
        <a href="#main-content" class="skip-link">Skip to main content</a>
        <a href="#contact-info" class="skip-link">Skip to contact information</a>
    `;
    skipLinks.style.cssText = `
        position: absolute;
        top: -100px;
        left: 0;
        z-index: 1002;
    `;

    document.body.insertBefore(skipLinks, document.body.firstChild);

    // Style skip links
    const skipLinkStyles = document.createElement('style');
    skipLinkStyles.textContent = `
        .skip-link {
            position: absolute;
            top: -100px;
            left: 10px;
            background: var(--accent-color);
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 500;
            transition: top 0.3s ease;
        }
        .skip-link:focus {
            top: 10px;
        }
    `;
    document.head.appendChild(skipLinkStyles);
});