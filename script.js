document.addEventListener('DOMContentLoaded', function() {

    initializeApp();

    window.addEventListener('scroll', handleScroll);

    setupIntersectionObserver();
});

function initializeApp() {
    console.log('Discord AI Setup Guide initialized');

    const stepCards = document.querySelectorAll('.step-card');
    stepCards.forEach(card => {
        card.addEventListener('click', function() {
            const stepNumber = this.getAttribute('data-step');
            showStepDetails(stepNumber);
        });
    });

    const methodSteps = document.querySelectorAll('.method-step');
    methodSteps.forEach(step => {
        step.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px) scale(1.02)';
        });

        step.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0) scale(1)';
        });
    });
}

function handleScroll() {
    const sections = document.querySelectorAll('.section');
    const navButtons = document.querySelectorAll('.nav-btn');

    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.clientHeight;

        if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    navButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(currentSection)) {
            btn.classList.add('active');
        }
    });
}

function setupIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        observer.observe(section);
    });
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

        updateNavigationActive(sectionId);
    }
}

function updateNavigationActive(sectionId) {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(sectionId)) {
            btn.classList.add('active');
        }
    });
}

function showStepDetails(stepNumber) {

    const stepCard = document.querySelector(`[data-step="${stepNumber}"]`);

    stepCard.style.transform = 'scale(1.05)';
    stepCard.style.boxShadow = '0 25px 50px rgba(102, 126, 234, 0.4)';

    setTimeout(() => {
        stepCard.style.transform = 'scale(1)';
        stepCard.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
    }, 300);

    console.log(`Step ${stepNumber} clicked`);
}

function selectMethod(methodNumber) {
    const methodButtons = document.querySelectorAll('.method-btn');
    const selectedButton = event.target.closest('.method-btn');

    methodButtons.forEach(btn => {
        btn.classList.remove('loading');
        btn.disabled = false;
    });

    selectedButton.classList.add('loading');
    selectedButton.disabled = true;

    setTimeout(() => {
        selectedButton.classList.remove('loading');
        selectedButton.disabled = false;

        showSuccessMessage(`Method ${methodNumber} selected successfully!`);

        setTimeout(() => {
            scrollToSection('finish');
        }, 1000);

    }, 2000);
}

function completeSetup() {
    const finishBtn = event.target.closest('.finish-btn');

    finishBtn.classList.add('loading');
    finishBtn.disabled = true;

    setTimeout(() => {
        finishBtn.classList.remove('loading');
        finishBtn.disabled = false;

        showCompletionMessage();

        addCelebrationAnimation();

    }, 3000);
}

function showSuccessMessage(message) {

    const notification = document.createElement('div');
    notification.className = 'success-notification';
    notification.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.4);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function showCompletionMessage() {

    const modal = document.createElement('div');
    modal.className = 'completion-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <i class="fas fa-trophy"></i>
                <h2>Setup Complete!</h2>
            </div>
            <div class="modal-body">
                <p>🎉 Congratulations! Your Discord AI bot is now ready to use.</p>
                <div class="completion-features">
                    <div class="feature">
                        <i class="fas fa-check-circle"></i>
                        <span>Bot is online and responsive</span>
                    </div>
                    <div class="feature">
                        <i class="fas fa-check-circle"></i>
                        <span>All permissions configured</span>
                    </div>
                    <div class="feature">
                        <i class="fas fa-check-circle"></i>
                        <span>Ready for production use</span>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button onclick="closeModal()" class="modal-btn">
                    <i class="fas fa-times"></i>
                    Close
                </button>
            </div>
        </div>
    `;

    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;

    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.cssText = `
        background: white;
        border-radius: 20px;
        padding: 40px;
        max-width: 500px;
        width: 90%;
        text-align: center;
        transform: scale(0.8);
        transition: transform 0.3s ease;
    `;

    document.body.appendChild(modal);

    setTimeout(() => {
        modal.style.opacity = '1';
        modalContent.style.transform = 'scale(1)';
    }, 100);
}

function closeModal() {
    const modal = document.querySelector('.completion-modal');
    if (modal) {
        modal.style.opacity = '0';
        const modalContent = modal.querySelector('.modal-content');
        modalContent.style.transform = 'scale(0.8)';

        setTimeout(() => {
            document.body.removeChild(modal);
        }, 300);
    }
}

function addCelebrationAnimation() {

    for (let i = 0; i < 50; i++) {
        createConfetti();
    }
}

function createConfetti() {
    const confetti = document.createElement('div');
    confetti.style.cssText = `
        position: fixed;
        width: 10px;
        height: 10px;
        background: ${getRandomColor()};
        top: -10px;
        left: ${Math.random() * window.innerWidth}px;
        z-index: 9999;
        border-radius: 50%;
        animation: confetti-fall 3s linear forwards;
    `;

    document.body.appendChild(confetti);

    setTimeout(() => {
        if (confetti.parentNode) {
            document.body.removeChild(confetti);
        }
    }, 3000);
}

function getRandomColor() {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'];
    return colors[Math.floor(Math.random() * colors.length)];
}

const style = document.createElement('style');
style.textContent = `
    @keyframes confetti-fall {
        0% {
            transform: translateY(-10px) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

document.addEventListener('keydown', function(event) {
    switch(event.key) {
        case 'ArrowUp':
            event.preventDefault();
            navigateSections('up');
            break;
        case 'ArrowDown':
            event.preventDefault();
            navigateSections('down');
            break;
        case '1':
            scrollToSection('steps');
            break;
        case '2':
            scrollToSection('methods');
            break;
        case '3':
            scrollToSection('finish');
            break;
    }
});

function navigateSections(direction) {
    const sections = ['steps', 'methods', 'finish'];
    const currentSection = getCurrentSection();
    const currentIndex = sections.indexOf(currentSection);

    let nextIndex;
    if (direction === 'up') {
        nextIndex = currentIndex > 0 ? currentIndex - 1 : sections.length - 1;
    } else {
        nextIndex = currentIndex < sections.length - 1 ? currentIndex + 1 : 0;
    }

    scrollToSection(sections[nextIndex]);
}

function getCurrentSection() {
    const sections = document.querySelectorAll('.section');
    let currentSection = 'steps';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.clientHeight;

        if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    return currentSection;
}

let touchStartY = 0;
let touchEndY = 0;

document.addEventListener('touchstart', function(event) {
    touchStartY = event.changedTouches[0].screenY;
});

document.addEventListener('touchend', function(event) {
    touchEndY = event.changedTouches[0].screenY;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartY - touchEndY;

    if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {

            navigateSections('down');
        } else {

            navigateSections('up');
        }
    }
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

window.addEventListener('scroll', throttle(handleScroll, 100));

function showImageModal(imageSrc, title) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalCommand = document.getElementById('modalCommand');
    const modalCommandText = document.getElementById('modalCommandText');
    const modalNote = document.getElementById('modalNote');
    const modalNoteText = document.getElementById('modalNoteText');

    modalImage.src = imageSrc;
    modalTitle.textContent = title;

    const method1Commands = {
        'images/Method_1.1.png': 'git clone git@github.com:xynnpg/DiscordAI.git',
        'images/Method_1.2.png': 'cd DiscordAI',
        'images/Method_1.3.png': 'nano .env',
        'images/Method_1.4.png': 'pip install -r requirements.txt',
        'images/Method_1.5.png': 'python run.py'
    };

    const method1Notes = {
        'images/Method_1.3.png': 'Or open it in notepad on Windows'
    };

    if (method1Commands[imageSrc]) {
        modalCommandText.textContent = method1Commands[imageSrc];
        modalCommand.style.display = 'flex';

        if (method1Notes[imageSrc]) {
            modalNoteText.textContent = method1Notes[imageSrc];
            modalNote.style.display = 'flex';
        } else {
            modalNote.style.display = 'none';
        }
    } else {
        modalCommand.style.display = 'none';
        modalNote.style.display = 'none';
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    document.addEventListener('keydown', handleModalKeydown);
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';

    document.removeEventListener('keydown', handleModalKeydown);
}

function handleModalKeydown(event) {
    if (event.key === 'Escape') {
        closeImageModal();
    }
}

document.addEventListener('click', function(event) {
    const modal = document.getElementById('imageModal');
    const modalContainer = modal.querySelector('.modal-image-container');

    if (event.target === modal) {
        closeImageModal();
    }
});

function copyCommand(command) {
    navigator.clipboard.writeText(command).then(function() {

        showCopySuccess();
    }).catch(function(err) {
        console.error('Could not copy text: ', err);

        fallbackCopyTextToClipboard(command);
    });
}

function showCopySuccess() {

    const notification = document.createElement('div');
    notification.className = 'copy-notification';
    notification.innerHTML = `
        <i class="fas fa-check"></i>
        <span>Command copied to clipboard!</span>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 2000);
}

function copyModalCommand() {
    const modalCommandText = document.getElementById('modalCommandText');
    const command = modalCommandText.textContent;

    if (command) {
        copyCommand(command);
    }
}

function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess();
        }
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
    }

    document.body.removeChild(textArea);
}