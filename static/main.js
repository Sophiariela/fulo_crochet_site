document.addEventListener('DOMContentLoaded', function() {
    const filtros = document.querySelectorAll('.filtro-btn');
    const cards = document.querySelectorAll('.card');
    filtros.forEach(filtro => {
        filtro.addEventListener('click', function() {
            filtros.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            const categoria = this.getAttribute('data-categoria');
            cards.forEach(card => {
                const cardCategoria = card.getAttribute('data-categoria');
                if (categoria === 'todos' || cardCategoria === categoria) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeInUp 0.6s ease-out';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});
