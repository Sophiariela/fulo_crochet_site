document.addEventListener('DOMContentLoaded', function () {
    const filtros = document.querySelectorAll('.filtro-btn');
    const cards = document.querySelectorAll('.card');

    filtros.forEach(function (filtro) {
        filtro.addEventListener('click', function () {
            filtros.forEach(function (f) { f.classList.remove('active'); });
            this.classList.add('active');
            var categoria = this.getAttribute('data-categoria');
            cards.forEach(function (card) {
                if (categoria === 'todos' || card.getAttribute('data-categoria') === categoria) {
                    card.style.display = 'block';
                    card.style.animation = 'none';
                    card.offsetHeight;
                    card.style.animation = 'fadeInUp 0.5s ease-out both';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});
