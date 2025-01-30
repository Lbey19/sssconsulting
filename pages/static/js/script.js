document.addEventListener("DOMContentLoaded", function () {
    // Initialisation AOS
    AOS.init({
        duration: 1000,
        once: true,
        easing: 'ease-out-quad'
    });

    // Animation texte optimisée
    const textElement = document.getElementById("animated-text");
    if (!textElement) {
        console.error("❌ #animated-text introuvable");
        return;
    }

    const words = [
        "Bienvenue chez SSS Consulting", 
        "Sécurisation de vos données", 
        "Solutions de cybersécurité"
    ];

    let wordIndex = 0;
    let letterIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function typeWriter() {
        const currentWord = words[wordIndex];
        
        if (!isDeleting) {
            textElement.textContent = currentWord.substring(0, letterIndex++);
        } else {
            textElement.textContent = currentWord.substring(0, letterIndex--);
        }

        // Gestion des transitions
        if (letterIndex === currentWord.length + 1) {
            isDeleting = true;
            typingSpeed = 2000;
        } else if (letterIndex === -1) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typingSpeed = 500;
        }

        setTimeout(typeWriter, isDeleting ? 50 : typingSpeed);
    }

    // Démarrer après le chargement complet
    setTimeout(typeWriter, 1000);

    // Gestion du scroll navbar
    let lastScroll = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        navbar.style.transform = currentScroll > lastScroll && currentScroll > 100 ? 
            'translateY(-100%)' : 
            'translateY(0)';
        lastScroll = currentScroll;
    });
});