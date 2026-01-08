import Link from 'next/link'

export function Navigation() {
  return (
    <nav className="bg-gray-800 text-white">
      <div className="container mx-auto px-4 py-3">
        <ul className="flex space-x-6">
          <li>
            <Link href="/dashboard" className="hover:text-gray-300">
              Home
            </Link>
          </li>
          <li>
            <Link href="/profile" className="hover:text-gray-300">
              Profile
            </Link>
          </li>
          <li>
            <Link href="/settings" className="hover:text-gray-300">
              Settings
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}