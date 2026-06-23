// side.js (Updated with Dropdown Functionality)

document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.getElementById('sidebar-toggle');
    const adminLayout = document.querySelector('.admin-layout');

    if (!sidebar || !toggleButton || !adminLayout) {
        return;
    }

    // Apply saved sidebar state immediately (no transition) to prevent flash
    let savedState = null;
    try { savedState = localStorage.getItem('sidebarState'); } catch (e) { /* Safari private */ }
    if (savedState === 'collapsed') {
        sidebar.classList.add('collapsed');
        adminLayout.classList.add('sidebar-collapsed');
    }
    // Re-enable transitions after state applied
    requestAnimationFrame(() => {
        document.documentElement.classList.remove('sidebar-pre-collapsed');
    });

    // --- Logic for Sidebar Collapse/Expand ---
    const toggleSidebar = () => {
        sidebar.classList.toggle('collapsed');
        adminLayout.classList.toggle('sidebar-collapsed');
        try {
            localStorage.setItem('sidebarState', sidebar.classList.contains('collapsed') ? 'collapsed' : 'expanded');
        } catch (e) { /* Safari private */ }

        // Close all dropdowns when collapsing sidebar
        if (sidebar.classList.contains('collapsed')) {
            const openDropdowns = document.querySelectorAll('.has-dropdown.open');
            openDropdowns.forEach(dropdown => {
                dropdown.classList.remove('open');
            });
        }
    };

    toggleButton.addEventListener('click', toggleSidebar);

    // --- NEW: Dropdown Functionality ---
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const parentLi = toggle.closest('.has-dropdown');
            const isOpen = parentLi.classList.contains('open');

            // Close all other dropdowns
            const allDropdowns = document.querySelectorAll('.has-dropdown');
            allDropdowns.forEach(dropdown => {
                if (dropdown !== parentLi) {
                    dropdown.classList.remove('open');
                }
            });

            // Toggle current dropdown
            if (isOpen) {
                parentLi.classList.remove('open');
            } else {
                parentLi.classList.add('open');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.has-dropdown')) {
            const openDropdowns = document.querySelectorAll('.has-dropdown.open');
            openDropdowns.forEach(dropdown => {
                dropdown.classList.remove('open');
            });
        }
    });

    // --- Logic for Active Navigation Link ---
    const navLinks = document.querySelectorAll('.nav-links li');
    const dropdownItems = document.querySelectorAll('.dropdown-menu li');

    // Function to clear all active states
    function clearAllActiveStates() {
        navLinks.forEach(item => {
            item.classList.remove('active');
        });
        dropdownItems.forEach(item => {
            item.classList.remove('active');
        });
        // Remove has-active-child class from all dropdowns
        document.querySelectorAll('.has-dropdown').forEach(dropdown => {
            dropdown.classList.remove('has-active-child');
        });
    }

    // Handle main navigation clicks
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Don't set active state for dropdown toggles
            if (!e.target.closest('.dropdown-toggle')) {
                clearAllActiveStates();
                link.classList.add('active');
            }
        });
    });

    // Handle dropdown item clicks
    dropdownItems.forEach(item => {
        item.addEventListener('click', (e) => {
            clearAllActiveStates();
            item.classList.add('active');

            // Mark parent dropdown as having active child and keep it open
            const parentDropdown = item.closest('.has-dropdown');
            if (parentDropdown) {
                parentDropdown.classList.add('has-active-child');
                parentDropdown.classList.add('open');
            }
        });
    });

    // Set active state based on current URL (for Django integration)
    const currentPath = window.location.pathname;

    // First check dropdown items (most specific match wins)
    let foundActiveItem = false;
    dropdownItems.forEach(item => {
        const linkHref = item.querySelector('a')?.getAttribute('href');
        if (linkHref && linkHref !== '/' && linkHref !== '#' && currentPath.startsWith(linkHref)) {
            clearAllActiveStates();
            item.classList.add('active');

            // Mark parent dropdown as having active child
            const parentDropdown = item.closest('.has-dropdown');
            if (parentDropdown) {
                parentDropdown.classList.add('has-active-child');
                parentDropdown.classList.add('open'); // Keep dropdown open
            }
            foundActiveItem = true;
        }
    });

    // If no dropdown item was active, check main navigation items
    if (!foundActiveItem) {
        navLinks.forEach(link => {
            const linkHref = link.querySelector('a')?.getAttribute('href');
            if (linkHref && linkHref !== '/' && linkHref !== '#' && currentPath.startsWith(linkHref)) {
                clearAllActiveStates();
                link.classList.add('active');
            }
        });
    }

});