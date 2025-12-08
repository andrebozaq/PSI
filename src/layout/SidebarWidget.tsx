export default function SidebarWidget() {
  return (
    <div
      className={`
        mx-auto mb-10 w-full max-w-60 rounded-2xl bg-gray-50 px-4 py-5 text-center dark:bg-white/[0.03]`}
    >
      <h3 className="mb-2 font-semibold text-gray-900 dark:text-white">
        Software #1 para soportes de recipientes a presión
      </h3>
      <p className="mb-4 text-gray-500 text-theme-sm dark:text-gray-400">
        Si te parece útil esta herramienta, considera donar un cafecito.
      </p>
      <a
        href="https://api.whatsapp.com/send?phone=584121262824&text=Estoy%20interesado%20en%20hacer%20una%20donaci%C3%B3n%20%F0%9F%98%81%F0%9F%99%8F"
        target="_blank"
        rel="nofollow"
        className="flex items-center justify-center p-3 font-medium text-white rounded-lg bg-brand-500 text-theme-sm hover:bg-brand-600"
      >
        Donar
      </a>
    </div>
  );
}
