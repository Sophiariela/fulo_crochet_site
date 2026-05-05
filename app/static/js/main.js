document.addEventListener('DOMContentLoaded', () => {
    const botoesFiltro = document.querySelectorAll('.filter-btn');
    const produtos = document.querySelectorAll('.product-card');

    botoesFiltro.forEach(botao => {
        botao.addEventListener('click', () => {
            // Remove active class from all buttons
            botoesFiltro.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            botao.classList.add('active');

            const categoria = botao.getAttribute('data-categoria');

            produtos.forEach(produto => {
                const produtoCategoria = produto.getAttribute('data-categoria');
                
                if (categoria === 'todos' || categoria === produtoCategoria) {
                    produto.style.display = 'block';
                    // Optional: add a small fade in animation
                    produto.style.opacity = '0';
                    setTimeout(() => {
                        produto.style.opacity = '1';
                        produto.style.transition = 'opacity 0.4s ease';
                    }, 10);
                } else {
                    produto.style.display = 'none';
                }
            });
        });
    });
});
