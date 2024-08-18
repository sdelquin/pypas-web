document.addEventListener("DOMContentLoaded", function (event) {
  // anchorjs
  anchors.add("h1,h2,h3,h4,h5,h6");

  // highlightjs-copy
  hljs.addPlugin(
    new CopyButtonPlugin({
      hook: (text, el) => {
        return text.replace(/^ *\$/, "");
      },
    })
  );
  hljs.highlightAll();

  // scroll to top: https://bit.ly/4cqyq7b y https://jsfiddle.net/nzms7y01/
  function toggleTopButton() {
    let scrollToTopBtn = document.getElementById("scrollToTopBtn");
    if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
    ) {
      scrollToTopBtn.style.display = "block";
    } else {
      scrollToTopBtn.style.display = "none";
    }
  }
  function scrollToTop() {
    let rootElement = document.documentElement;
    rootElement.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }
  let scrollToTopBtn = document.getElementById("scrollToTopBtn");
  // window.onscroll = function() {toggleTopButton()};
  window.addEventListener("scroll", toggleTopButton);
  scrollToTopBtn.addEventListener("click", scrollToTop);
});
