import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup, within } from "@testing-library/react";
import { OwnerManagement } from "./OwnerManagement";

const inventory = [
  {
    id: 1,
    name: "Milk",
    unit: "ml",
    stock_quantity: 5000,
    reorder_level: 500,
    active: true,
    unit_editable: true,
    convertible_units: ["ml", "l"],
  },
];

const menu = [
  {
    id: 1,
    name: "Latte",
    price: 4500,
    active: true,
    recipe: [
      { ingredient_id: 1, ingredient_name: "Milk", quantity: 200 },
    ],
  },
];

const onMenuChanged = vi.fn().mockResolvedValue(undefined);
const onInventoryChanged = vi.fn().mockResolvedValue(undefined);

function mockFetch() {
  return vi.fn(async (url: string | URL | Request, options?: RequestInit) => {
    const path = String(url);
    const method = options?.method ?? "GET";

    if (path.endsWith("/owner/inventory") && method === "GET") {
      return Response.json(inventory);
    }

    if (path.endsWith("/owner/menu") && method === "GET") {
      return Response.json(menu);
    }

    if (path.endsWith("/owner/inventory") && method === "POST") {
      return Response.json({
        id: 2,
        name: "Matcha powder",
        unit: "g",
        stock_quantity: 1000,
        reorder_level: 100,
        active: true,
      });
    }

    if (path.endsWith("/owner/menu") && method === "POST") {
      return Response.json({
        id: 2,
        name: "Matcha Latte",
        price: 5500,
        active: true,
        recipe: [
          { ingredient_id: 1, ingredient_name: "Milk", quantity: 200 },
        ],
      });
    }

    return Response.json({ detail: "Not found" }, { status: 404 });
  });
}

describe("OwnerManagement", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", mockFetch());
    onMenuChanged.mockClear();
    onInventoryChanged.mockClear();
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("loads inventory and menu from the API", async () => {
    render(
      <OwnerManagement
        onMenuChanged={onMenuChanged}
        onInventoryChanged={onInventoryChanged}
      />,
    );

    expect(await screen.findByText("Latte")).toBeInTheDocument();
    expect(screen.getByText("Milk")).toBeInTheDocument();
  });

  it("adds an ingredient using the correct API payload", async () => {
    const fetchMock = mockFetch();
    vi.stubGlobal("fetch", fetchMock);

    render(
      <OwnerManagement
        onMenuChanged={onMenuChanged}
        onInventoryChanged={onInventoryChanged}
      />,
    );

    await screen.findByText("Latte");

    fireEvent.click(screen.getByText("Add ingredient", { selector: "summary" }));

    fireEvent.change(screen.getByPlaceholderText("e.g. Matcha powder"), {
      target: { value: "Matcha powder" },
    });

    fireEvent.change(screen.getByLabelText("Starting stock (g)"), {
      target: { value: "1000" },
    });

    fireEvent.change(screen.getByLabelText("Low-stock threshold (g)"), {
      target: { value: "100" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Add ingredient" }));

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining("/owner/inventory"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            name: "Matcha powder",
            unit: "g",
            stock_quantity: 1000,
            reorder_level: 100,
          }),
        }),
      );
    });

    expect(await screen.findByText("Matcha powder was saved in inventory."))
      .toBeInTheDocument();
    expect(onInventoryChanged).toHaveBeenCalledOnce();
  });

  it("adds a menu item with its recipe", async () => {
    const fetchMock = mockFetch();
    vi.stubGlobal("fetch", fetchMock);

    render(
      <OwnerManagement
        onMenuChanged={onMenuChanged}
        onInventoryChanged={onInventoryChanged}
      />,
    );

    await screen.findByText("Latte");

    fireEvent.click(screen.getByText("Add menu item", { selector: "summary" }));

    fireEvent.change(screen.getByPlaceholderText("e.g. Matcha Latte"), {
      target: { value: "Matcha Latte" },
    });

    fireEvent.change(screen.getByLabelText("Price (KRW)"), {
      target: { value: "5500" },
    });

    fireEvent.change(screen.getByLabelText("Ingredient"), {
      target: { value: "1" },
    });

    fireEvent.change(screen.getByLabelText("Quantity"), {
      target: { value: "200" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Add menu item" }));

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining("/owner/menu"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            name: "Matcha Latte",
            price: 5500,
            recipe: [
              { ingredient_id: 1, quantity: 200, unit: "ml" },
            ],
          }),
        }),
      );
    });

    expect(await screen.findByText(
      "Matcha Latte is now available on the cashier menu.",
    )).toBeInTheDocument();

    expect(onMenuChanged).toHaveBeenCalledOnce();
  });

  it("does not delete a menu item when removal is cancelled", async () => {
    const fetchMock = mockFetch();
    vi.stubGlobal("fetch", fetchMock);
    vi.stubGlobal("confirm", vi.fn(() => false));

    render(
      <OwnerManagement
        onMenuChanged={onMenuChanged}
        onInventoryChanged={onInventoryChanged}
      />,
    );

    await screen.findByText("Latte");

    const menuCard = screen.getByRole("heading", { name: "Menu items" }).closest("article");
    fireEvent.click(within(menuCard!).getByRole("button", { name: "Remove" }));

    expect(window.confirm).toHaveBeenCalledOnce();
    expect(fetchMock).not.toHaveBeenCalledWith(
      expect.stringContaining("/owner/menu/1"),
      expect.objectContaining({ method: "DELETE" }),
    );
  });
});
