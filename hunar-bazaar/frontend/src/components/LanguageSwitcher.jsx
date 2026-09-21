import { useTranslation } from "react-i18next";

export default function LanguageSwitcher() {
  const { i18n } = useTranslation();
  return (
    <select
      value={i18n.language}
      onChange={(e) => i18n.changeLanguage(e.target.value)}
      className="bg-transparent border border-brass/40 text-cream text-sm rounded px-2 py-1"
      aria-label="Select language"
    >
      <option value="en">EN</option>
      <option value="hi">हिं</option>
    </select>
  );
}
