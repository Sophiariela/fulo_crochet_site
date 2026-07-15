document.addEventListener('DOMContentLoaded', () => {
    // FILTERS
    const botoesFiltro = document.querySelectorAll('.filter-btn');
    const produtos = document.querySelectorAll('.product-card');

    if (botoesFiltro.length > 0) {
        botoesFiltro.forEach(botao => {
            botao.addEventListener('click', () => {
                botoesFiltro.forEach(b => b.classList.remove('active'));
                botao.classList.add('active');

                const categoria = botao.getAttribute('data-categoria');

                produtos.forEach(produto => {
                    const produtoCategoria = produto.getAttribute('data-categoria');
                    
                    if (categoria === 'todos' || categoria === produtoCategoria) {
                        produto.style.display = 'block';
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
    }

    // SHIPPING CALCULATION
    const btn = document.getElementById('calculate-shipping');

    if (btn) {
        btn.addEventListener('click', async () => {
            const cepInput = document.getElementById('cep');
            const result = document.getElementById('shipping-result');

            let cep = cepInput.value.replace(/\D/g, '');

            if (cep.length !== 8) {
                result.innerHTML = `
                    <span class="shipping-error">
                        Digite um CEP válido
                    </span>
                `;
                return;
            }

            result.innerHTML = 'Calculando...';

            try {
                const response = await fetch(
                    `https://viacep.com.br/ws/${cep}/json/`
                );

                const data = await response.json();

                if (data.erro) {
                    result.innerHTML = `
                        <span class="shipping-error">
                            CEP não encontrado
                        </span>
                    `;
                    return;
                }

                const uf = data.uf;

                let price = 0;
                let prazo = '';

                const norte = ['AC','AP','AM','PA','RO','RR','TO'];
                const nordeste = ['AL','BA','CE','MA','PB','PE','PI','RN','SE'];
                const centro = ['DF','GO','MT','MS'];
                const sudeste = ['SP','RJ','MG','ES'];
                const sul = ['PR','RS','SC'];

                if (norte.includes(uf)) {
                    price = 34.90;
                    prazo = '8 a 12 dias úteis';
                }
                else if (nordeste.includes(uf)) {
                    price = 29.90;
                    prazo = '5 a 8 dias úteis';
                }
                else if (centro.includes(uf)) {
                    price = 27.90;
                    prazo = '4 a 7 dias úteis';
                }
                else if (sudeste.includes(uf)) {
                    price = 19.90;
                    prazo = '2 a 5 dias úteis';
                }
                else if (sul.includes(uf)) {
                    price = 24.90;
                    prazo = '3 a 6 dias úteis';
                }

                result.innerHTML = `
                    <div class="shipping-success">
                        <strong>${data.localidade} - ${uf}</strong>
                        <br><br>
                        Frete estimado:
                        <strong>
                            R$ ${price.toFixed(2)}
                        </strong>
                        <br>
                        Entrega em:
                        <strong>
                            ${prazo}
                        </strong>
                    </div>
                `;

            } catch (error) {
                result.innerHTML = `
                    <span class="shipping-error">
                        Erro ao calcular frete
                    </span>
                `;
            }
        });
    }
});
