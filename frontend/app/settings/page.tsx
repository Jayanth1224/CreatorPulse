"use client";

import { useState } from "react";
import { Navigation } from "@/components/layout/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { tonePresets } from "@/lib/mock-data";
import { Check, Mail, AlertCircle, Upload } from "lucide-react";

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState<string>("account");

  return (
    <>
      <Navigation />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold mb-2">Settings</h1>
          <p className="text-muted">
            Manage your account, preferences, and integrations.
          </p>
        </div>

        <div className="grid lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <nav className="lg:col-span-1 space-y-1">
            <NavButton
              active={activeSection === "account"}
              onClick={() => setActiveSection("account")}
            >
              Account
            </NavButton>
            <NavButton
              active={activeSection === "esp"}
              onClick={() => setActiveSection("esp")}
            >
              Email Provider
            </NavButton>
            <NavButton
              active={activeSection === "recipients"}
              onClick={() => setActiveSection("recipients")}
            >
              Recipients
            </NavButton>
            <NavButton
              active={activeSection === "tone"}
              onClick={() => setActiveSection("tone")}
            >
              Tone & Voice
            </NavButton>
            <NavButton
              active={activeSection === "billing"}
              onClick={() => setActiveSection("billing")}
            >
              Billing & Plan
            </NavButton>
          </nav>

          {/* Content */}
          <div className="lg:col-span-3 space-y-6">
            {activeSection === "account" && <AccountSection />}
            {activeSection === "esp" && <ESPSection />}
            {activeSection === "recipients" && <RecipientsSection />}
            {activeSection === "tone" && <ToneSection />}
            {activeSection === "billing" && <BillingSection />}
          </div>
        </div>
      </main>
    </>
  );
}

function NavButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
        active
          ? "bg-primary text-white"
          : "text-muted hover:bg-surface hover:text-foreground"
      }`}
    >
      {children}
    </button>
  );
}

function AccountSection() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Account Settings</CardTitle>
        <CardDescription>
          Manage your personal information and preferences
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="name">Full Name</Label>
          <Input
            id="name"
            defaultValue="Jayanth Bandi"
            className="mt-2"
          />
        </div>
        <div>
          <Label htmlFor="email">Email Address</Label>
          <Input
            id="email"
            type="email"
            defaultValue="jayanth@example.com"
            className="mt-2"
          />
        </div>
        <div>
          <Label htmlFor="timezone">Timezone</Label>
          <Select id="timezone" className="mt-2" defaultValue="America/Los_Angeles">
            <option value="America/Los_Angeles">Pacific Time (PT)</option>
            <option value="America/Denver">Mountain Time (MT)</option>
            <option value="America/Chicago">Central Time (CT)</option>
            <option value="America/New_York">Eastern Time (ET)</option>
            <option value="Europe/London">London (GMT)</option>
            <option value="Asia/Kolkata">India (IST)</option>
          </Select>
          <p className="text-xs text-muted mt-2">
            Used for scheduling draft delivery times
          </p>
        </div>
        <Button>Save Changes</Button>
      </CardContent>
    </Card>
  );
}

function ESPSection() {
  const [provider, setProvider] = useState<string>("sendgrid");
  const [isConnected, setIsConnected] = useState(false);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Email Service Provider</CardTitle>
        <CardDescription>
          Connect your email provider to send newsletters
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="provider">Provider</Label>
          <Select
            id="provider"
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            className="mt-2"
          >
            <option value="sendgrid">SendGrid</option>
            <option value="mailgun">Mailgun</option>
            <option value="smtp">SMTP (Generic)</option>
          </Select>
        </div>

        {provider === "sendgrid" && (
          <div>
            <Label htmlFor="api-key">SendGrid API Key</Label>
            <Input
              id="api-key"
              type="password"
              placeholder="SG.xxxxxxxxxxxxxxxxxxxxx"
              className="mt-2"
            />
          </div>
        )}

        {provider === "mailgun" && (
          <>
            <div>
              <Label htmlFor="mailgun-domain">Domain</Label>
              <Input
                id="mailgun-domain"
                placeholder="mg.yourdomain.com"
                className="mt-2"
              />
            </div>
            <div>
              <Label htmlFor="mailgun-key">API Key</Label>
              <Input
                id="mailgun-key"
                type="password"
                placeholder="key-xxxxxxxxxxxxxxxxxxxxx"
                className="mt-2"
              />
            </div>
          </>
        )}

        {provider === "smtp" && (
          <>
            <div>
              <Label htmlFor="smtp-host">SMTP Host</Label>
              <Input
                id="smtp-host"
                placeholder="smtp.example.com"
                className="mt-2"
              />
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="smtp-port">Port</Label>
                <Input id="smtp-port" placeholder="587" className="mt-2" />
              </div>
              <div>
                <Label htmlFor="smtp-username">Username</Label>
                <Input id="smtp-username" placeholder="user@example.com" className="mt-2" />
              </div>
            </div>
            <div>
              <Label htmlFor="smtp-password">Password</Label>
              <Input
                id="smtp-password"
                type="password"
                placeholder="••••••••"
                className="mt-2"
              />
            </div>
          </>
        )}

        <div className="flex items-center gap-2">
          <Button onClick={() => setIsConnected(!isConnected)}>
            {isConnected ? "Disconnect" : "Connect & Verify"}
          </Button>
          {isConnected && (
            <Badge variant="success" className="flex items-center gap-1">
              <Check className="h-3 w-3" />
              Connected
            </Badge>
          )}
        </div>

        {isConnected && (
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4 flex items-start gap-3">
            <Mail className="h-5 w-5 text-green-600 dark:text-green-400 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-green-900 dark:text-green-100">
                Connection Verified
              </p>
              <p className="text-xs text-green-700 dark:text-green-300 mt-1">
                Your ESP is connected and ready to send newsletters.
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function RecipientsSection() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Default Recipient List</CardTitle>
        <CardDescription>
          Set your default recipient list for sending newsletters
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="recipient-list">Recipient Email or List</Label>
          <Input
            id="recipient-list"
            placeholder="newsletter@example.com"
            className="mt-2"
          />
          <p className="text-xs text-muted mt-2">
            Enter a single email address or your mailing list address
          </p>
        </div>
        <div>
          <Label htmlFor="from-name">From Name</Label>
          <Input
            id="from-name"
            placeholder="Your Name"
            defaultValue="Jayanth Bandi"
            className="mt-2"
          />
        </div>
        <div>
          <Label htmlFor="from-email">From Email</Label>
          <Input
            id="from-email"
            type="email"
            placeholder="you@example.com"
            defaultValue="jayanth@example.com"
            className="mt-2"
          />
        </div>
        <Button>Save Recipient Settings</Button>
      </CardContent>
    </Card>
  );
}

function ToneSection() {
  const [selectedTone, setSelectedTone] = useState("professional");

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Tone Preferences</CardTitle>
          <CardDescription>
            Choose your default writing tone for generated drafts
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid sm:grid-cols-2 gap-3">
            {tonePresets.map((preset) => (
              <button
                key={preset.value}
                onClick={() => setSelectedTone(preset.value)}
                className={`p-4 rounded-lg border-2 text-left transition-colors ${
                  selectedTone === preset.value
                    ? "border-primary bg-primary/5"
                    : "border-border hover:border-primary/50"
                }`}
              >
                <div className="font-semibold mb-1 flex items-center justify-between">
                  {preset.label}
                  {selectedTone === preset.value && (
                    <Check className="h-4 w-4 text-primary" />
                  )}
                </div>
                <div className="text-xs text-muted">{preset.description}</div>
              </button>
            ))}
          </div>
          <Button>Save Tone Preference</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Voice Training</CardTitle>
          <CardDescription>
            Upload samples of your writing to train a custom voice model
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer">
            <Upload className="h-8 w-8 text-muted mx-auto mb-3" />
            <p className="font-medium mb-1">Upload Writing Samples</p>
            <p className="text-xs text-muted mb-3">
              Upload at least 20 examples of your best newsletters or articles
            </p>
            <Button variant="outline" size="sm">
              Choose Files
            </Button>
          </div>
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-yellow-900 dark:text-yellow-100">
                Pro Feature
              </p>
              <p className="text-xs text-yellow-700 dark:text-yellow-300 mt-1">
                Voice training is available on the Pro plan. Upgrade to create a custom voice model.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function BillingSection() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Current Plan</CardTitle>
          <CardDescription>
            You're currently on the Free plan
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold text-lg">Free Plan</div>
                <div className="text-sm text-muted">1 topic bundle, basic summaries</div>
              </div>
              <Badge variant="secondary">Active</Badge>
            </div>
            <Button>Upgrade to Pro</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Available Plans</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="font-semibold">Pro Plan</div>
              <div className="text-2xl font-bold">$25<span className="text-sm text-muted">/mo</span></div>
            </div>
            <ul className="text-sm text-muted space-y-1 mb-4">
              <li>✓ Custom voice training</li>
              <li>✓ Advanced analytics</li>
              <li>✓ 3+ topic bundles</li>
              <li>✓ Priority support</li>
            </ul>
            <Button className="w-full">Upgrade Now</Button>
          </div>

          <div className="border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="font-semibold">Agency Plan</div>
              <div className="text-2xl font-bold">Custom</div>
            </div>
            <ul className="text-sm text-muted space-y-1 mb-4">
              <li>✓ Multi-newsletter support</li>
              <li>✓ Shared analytics</li>
              <li>✓ Unlimited bundles</li>
              <li>✓ Dedicated account manager</li>
            </ul>
            <Button variant="outline" className="w-full">Contact Sales</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

