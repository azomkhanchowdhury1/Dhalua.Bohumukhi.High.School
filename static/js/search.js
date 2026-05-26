/* START: SEARCH_SCRIPT */
document.addEventListener('DOMContentLoaded', function() {
    const searchBox = document.getElementById('globalSearchBox');
    const searchInput = document.getElementById('globalSearchInput');
    const closeSearch = document.getElementById('closeSearch');
    const searchResults = document.getElementById('searchResults');

    if (!searchBox || !searchInput) return;

    // Toggle search box
    searchBox.addEventListener('click', function(e) {
        if (!this.classList.contains('active')) {
            this.classList.add('active');
            searchInput.focus();
        }
    });

    // Close search box
    closeSearch.addEventListener('click', function(e) {
        e.stopPropagation();
        searchBox.classList.remove('active');
        searchInput.value = '';
        searchResults.classList.remove('active');
    });

    // Click outside to close
    document.addEventListener('click', function(e) {
        if (!searchBox.contains(e.target) && !searchResults.contains(e.target)) {
            searchBox.classList.remove('active');
            searchResults.classList.remove('active');
        }
    });

    // Handle search input
    let debounceTimer;
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }

        debounceTimer = setTimeout(() => {
            fetchSearchResults(query);
        }, 300);
    });

    function fetchSearchResults(query) {
        fetch(`/accounts/global-search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displayResults(data.results);
            })
            .catch(error => {
                console.error('Search error:', error);
            });
    }

    function displayResults(results) {
        searchResults.innerHTML = '';
        
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No results found</div>';
        } else {
            results.forEach(item => {
                const resultItem = document.createElement('a');
                resultItem.href = item.url;
                resultItem.className = 'result-item';
                
                // Get initials for avatar
                const initials = item.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

                resultItem.innerHTML = `
                    <div class="result-avatar">${initials}</div>
                    <div class="result-info">
                        <span class="result-name">${item.name}</span>
                        <span class="result-role">${item.role}</span>
                    </div>
                `;
                searchResults.appendChild(resultItem);
            });
        }
        
        searchResults.classList.add('active');
    }

    // START: PROFILE_DROPDOWN_LOGIC
    const profileTrigger = document.getElementById('profileTrigger');
    const profileDropdown = document.getElementById('profileDropdown');

    if (profileTrigger && profileDropdown) {
        profileTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('active');
            
            // Close search if open
            if (searchBox && searchBox.classList.contains('active')) {
                searchBox.classList.remove('active');
                searchResults.classList.remove('active');
            }
        });

        document.addEventListener('click', function(e) {
            if (!profileDropdown.contains(e.target) && !profileTrigger.contains(e.target)) {
                profileDropdown.classList.remove('active');
            }
        });
    }
    // END: PROFILE_DROPDOWN_LOGIC
});
/* END: SEARCH_SCRIPT */
