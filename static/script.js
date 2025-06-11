
    // Todo List Animations and Interactions
    class TodoAnimations {
        constructor() {
            this.init();
        }

        init() {
            this.setupTableAnimations();
            this.setupHoverEffects();
            this.setupButtonEffects();
            this.setupSearchEffects();
            this.observeNewTasks();
        }

        // Staggered slide-in animation for table rows
        setupTableAnimations() {
            const rows = document.querySelectorAll('.task-table tbody tr');

            rows.forEach((row, index) => {
                // Initial state
                row.style.opacity = '0';
                row.style.transform = 'translateY(20px)';
                row.style.transition = 'all 0.5s ease';

                // Animate in with delay
                setTimeout(() => {
                    row.style.opacity = '1';
                    row.style.transform = 'translateY(0)';
                }, index * 100 + 100);
            });
        }

        // Enhanced hover effects for table rows
        setupHoverEffects() {
            const rows = document.querySelectorAll('.task-table tbody tr');

            rows.forEach(row => {
                row.addEventListener('mouseenter', () => {
                    row.style.transform = 'translateY(-4px)';
                    row.style.background = 'rgba(102, 126, 234, 0.1)';
                    row.style.boxShadow = '0 8px 20px rgba(102, 126, 234, 0.3)';
                    row.style.transition = 'all 0.3s ease';
                });

                row.addEventListener('mouseleave', () => {
                    row.style.transform = 'translateY(0)';
                    row.style.background = '';
                    row.style.boxShadow = '';
                });
            });
        }

        // Button hover effects
        setupButtonEffects() {
            const buttons = document.querySelectorAll('.btn, .add-task-link');
            const actionLinks = document.querySelectorAll('.task-table td:last-child a');

            [...buttons, ...actionLinks].forEach(btn => {
                btn.addEventListener('mouseenter', () => {
                    btn.style.transform = 'translateY(-2px)';
                    btn.style.transition = 'all 0.3s ease';

                    if (btn.classList.contains('btn')) {
                        btn.style.boxShadow = '0 6px 20px rgba(79, 172, 254, 0.6)';
                    } else if (btn.classList.contains('add-task-link')) {
                        btn.style.boxShadow = '0 6px 20px rgba(72, 187, 120, 0.4)';
                    } else if (btn.classList.contains('edit-link')) {
                        btn.style.background = '#38a169';
                    } else if (btn.classList.contains('delete-link')) {
                        btn.style.background = '#e53e3e';
                    }
                });

                btn.addEventListener('mouseleave', () => {
                    btn.style.transform = 'translateY(0)';
                    btn.style.boxShadow = '';

                    if (btn.classList.contains('edit-link')) {
                        btn.style.background = '#48bb78';
                    } else if (btn.classList.contains('delete-link')) {
                        btn.style.background = '#f56565';
                    }
                });
            });
        }

        // Search input focus effects
        setupSearchEffects() {
            const searchInput = document.querySelector('.search-input');

            if (searchInput) {
                searchInput.addEventListener('focus', () => {
                    searchInput.style.boxShadow = '0 0 10px rgba(79, 172, 254, 0.5)';
                    searchInput.style.transition = 'all 0.3s ease';
                });

                searchInput.addEventListener('blur', () => {
                    searchInput.style.boxShadow = '';
                });
            }
        }

        // Animate new tasks when they're added dynamically
        animateNewTask(taskElement) {
            taskElement.style.opacity = '0';
            taskElement.style.transform = 'translateY(20px)';
            taskElement.style.transition = 'all 0.5s ease';

            // Trigger animation
            requestAnimationFrame(() => {
                taskElement.style.opacity = '1';
                taskElement.style.transform = 'translateY(0)';
            });

            // Add hover effects to new task
            this.addHoverEffect(taskElement);
        }

        // Add hover effect to a single row
        addHoverEffect(row) {
            row.addEventListener('mouseenter', () => {
                row.style.transform = 'translateY(-4px)';
                row.style.background = 'rgba(102, 126, 234, 0.1)';
                row.style.boxShadow = '0 8px 20px rgba(102, 126, 234, 0.3)';
                row.style.transition = 'all 0.3s ease';
            });

            row.addEventListener('mouseleave', () => {
                row.style.transform = 'translateY(0)';
                row.style.background = '';
                row.style.boxShadow = '';
            });
        }

        // Watch for dynamically added tasks
        observeNewTasks() {
            const tableBody = document.querySelector('.task-table tbody');

            if (tableBody) {
                const observer = new MutationObserver((mutations) => {
                    mutations.forEach((mutation) => {
                        if (mutation.type === 'childList') {
                            mutation.addedNodes.forEach((node) => {
                                if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'TR') {
                                    this.animateNewTask(node);
                                }
                            });
                        }
                    });
                });

                observer.observe(tableBody, { childList: true });
            }
        }

        // Smooth delete animation
        animateDelete(taskElement, callback) {
            taskElement.style.transform = 'translateX(-100%)';
            taskElement.style.opacity = '0';
            taskElement.style.transition = 'all 0.3s ease';

            setTimeout(() => {
                if (callback) callback();
            }, 300);
        }

        // Loading animation for buttons
        showButtonLoading(button) {
            const originalText = button.textContent;
            button.textContent = 'Loading...';
            button.style.opacity = '0.7';
            button.style.pointerEvents = 'none';

            return () => {
                button.textContent = originalText;
                button.style.opacity = '1';
                button.style.pointerEvents = 'auto';
            };
        }

        // Notification popup animation
        showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.textContent = message;
            notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            transform: translateX(100%);
            transition: all 0.3s ease;
            background: ${type === 'success' ? '#48bb78' : '#f56565'};
        `;

            document.body.appendChild(notification);

            // Animate in
            requestAnimationFrame(() => {
                notification.style.transform = 'translateX(0)';
            });

            // Auto remove
            setTimeout(() => {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 3000);
        }
    }

    // Initialize animations when DOM is loaded
    document.addEventListener('DOMContentLoaded', () => {
        window.todoAnimations = new TodoAnimations();
    });

    // Export functions for use in your app
    window.todoUtils = {
        animateDelete: (element, callback) => window.todoAnimations.animateDelete(element, callback),
        showLoading: (button) => window.todoAnimations.showButtonLoading(button),
        showNotification: (message, type) => window.todoAnimations.showNotification(message, type)
    };