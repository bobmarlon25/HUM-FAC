import { Building2, Menu, Plus, Search } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <header className="border-b">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-4">
              <Building2 className="h-6 w-6" />
              <h1 className="text-xl font-bold">Sistema de Proveedores</h1>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <Link href="/" className="text-sm font-medium">
                Inicio
              </Link>
              <Link href="/proveedores" className="text-sm font-medium">
                Proveedores
              </Link>
              <Link href="/reportes" className="text-sm font-medium">
                Reportes
              </Link>
              <Link href="/configuracion" className="text-sm font-medium">
                Configuración
              </Link>
            </div>
            <Button variant="ghost" className="md:hidden">
              <Menu className="h-6 w-6" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="flex flex-col space-y-8">
          {/* Search and Add Section */}
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="relative w-full sm:w-96">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Buscar proveedores..." className="pl-8" />
            </div>
            <Button>
              <Plus className="mr-2 h-4 w-4" /> Nuevo Proveedor
            </Button>
          </div>

          {/* Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Sample Cards - These would be mapped from your data */}
            <SupplierCard
              name="Proveedor 1"
              category="Materiales"
              contact="Juan Pérez"
              phone="+1 234 567 890"
              email="proveedor1@email.com"
              logoUrl="/placeholder.svg?height=100&width=200"
            />
            <SupplierCard
              name="Proveedor 2"
              category="Servicios"
              contact="María García"
              phone="+1 234 567 891"
              email="proveedor2@email.com"
              logoUrl="/placeholder.svg?height=100&width=200"
            />
            <SupplierCard
              name="Proveedor 3"
              category="Equipamiento"
              contact="Carlos López"
              phone="+1 234 567 892"
              email="proveedor3@email.com"
              logoUrl="/placeholder.svg?height=100&width=200"
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground">
              © 2024 Sistema de Gestión de Proveedores. Todos los derechos reservados.
            </p>
            <div className="flex items-center space-x-4">
              <Link href="/terminos" className="text-sm text-muted-foreground hover:text-primary">
                Términos
              </Link>
              <Link href="/privacidad" className="text-sm text-muted-foreground hover:text-primary">
                Privacidad
              </Link>
              <Link href="/contacto" className="text-sm text-muted-foreground hover:text-primary">
                Contacto
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

function SupplierCard({
  name,
  category,
  contact,
  phone,
  email,
  logoUrl = "/placeholder.svg?height=100&width=200",
}: {
  name: string
  category: string
  contact: string
  phone: string
  email: string
  logoUrl?: string
}) {
  return (
    <Card className="overflow-hidden">
      <div className="p-6 bg-muted flex justify-center items-center">
        <img src={logoUrl || "/placeholder.svg"} alt={`Logo de ${name}`} className="h-24 w-auto object-contain" />
      </div>
      <CardHeader>
        <CardTitle className="text-xl">{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-sm font-medium">Categoría:</span>
            <span className="text-sm">{category}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm font-medium">Contacto:</span>
            <span className="text-sm">{contact}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm font-medium">Teléfono:</span>
            <span className="text-sm">{phone}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm font-medium">Email:</span>
            <span className="text-sm">{email}</span>
          </div>
          <div className="flex justify-end pt-4">
            <Button variant="outline" size="sm">
              Ver Detalles
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

