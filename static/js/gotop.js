// получаем доступ к элементу кнопки "наверх"
const goTopBtn = document.querySelector("#go-top");

// обработчик события прокрутки окна
window.addEventListener("scroll", trackScroll);
// обработчик нажатия на кнопку (идём наверх)
goTopBtn.addEventListener("click", goTop);

function trackScroll() {
    // положение "верхушки" страницы
    const scrolled = window.scrollY;
    // высота клиентской области окна
    const coords = window.screen.height / 2;
    // если прокрутили на один экран, то кнопка появится
    if (scrolled > coords)
        goTopBtn.classList.add("go-top--show");
    else
        goTopBtn.classList.remove("go-top--show");
}

/* функция прокрутки наверх */
function goTop() {
    // если смещение есть (окно прокручено) 
    if(window.scrollY > 0) {
        // в этом случае "едем" наверх
        window.scrollTo(0, 0, behavior="smooth"); // прокручиваем до верху плавно
    }
}