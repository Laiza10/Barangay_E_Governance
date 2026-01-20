document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card-float');
    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width/2;
            const centerY = rect.height/2;
            const rotateX = ((y - centerY)/centerY) * 5;
            const rotateY = ((x - centerX)/centerX) * -5;
            card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(0)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'rotateX(0deg) rotateY(0deg) translateZ(0)';
        });
    });
});
