"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { X } from "lucide-react";

interface CreateBundleModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateBundle: (bundle: { key: string; label: string; description: string }) => void;
}

export function CreateBundleModal({ isOpen, onClose, onCreateBundle }: CreateBundleModalProps) {
  const [formData, setFormData] = useState({
    key: "",
    label: "",
    description: ""
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.key || !formData.label) return;

    setLoading(true);
    try {
      await onCreateBundle(formData);
      setFormData({ key: "", label: "", description: "" });
      onClose();
    } catch (error) {
      console.error("Error creating bundle:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyChange = (value: string) => {
    // Auto-generate key from label if empty
    const key = value.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
    setFormData(prev => ({ ...prev, key, label: value }));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-md w-full">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Create New Bundle</CardTitle>
              <Button variant="ghost" onClick={onClose}>
                <X className="h-5 w-5" />
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="label">Bundle Name</Label>
                <Input
                  id="label"
                  value={formData.label}
                  onChange={(e) => handleKeyChange(e.target.value)}
                  placeholder="e.g., AI & ML Trends"
                  required
                />
              </div>
              
              <div>
                <Label htmlFor="key">Bundle Key</Label>
                <Input
                  id="key"
                  value={formData.key}
                  onChange={(e) => setFormData(prev => ({ ...prev, key: e.target.value }))}
                  placeholder="e.g., ai-ml-trends"
                  required
                />
                <p className="text-xs text-muted mt-1">
                  Used internally to identify this bundle
                </p>
              </div>

              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Describe what this bundle covers..."
                  rows={3}
                />
              </div>

              <div className="flex gap-2 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={onClose}
                  className="flex-1"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  disabled={loading || !formData.key || !formData.label}
                  className="flex-1"
                >
                  {loading ? "Creating..." : "Create Bundle"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
